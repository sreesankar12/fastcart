from django.conf import settings
from oscar.core.loading import get_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import stripe
from django import http
from django.conf import settings

from django.utils.translation import gettext as _
from django.views import generic

from oscar.core.loading import get_class, get_classes, get_model
from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from .facade import Facade

from . import PAYMENT_METHOD_STRIPE, PAYMENT_EVENT_PURCHASE, STRIPE_EMAIL, STRIPE_TOKEN

from . import forms
from apps.order.models import Order
from apps.voucher.models import UserVouchers
from ..customer.models import Referrals, UserInvitation
from ..customer.utils import apply_voucher_to_cart
from ..voucher.models import ReferalVoucher
from django.utils import timezone


Applicator = get_class('offer.applicator', 'Applicator')
SourceType = get_model('payment', 'SourceType')
Source = get_model('payment', 'Source')
RedirectRequired, UnableToTakePayment, PaymentError \
    = get_classes('payment.exceptions', ['RedirectRequired',
                                         'UnableToTakePayment',
                                         'PaymentError'])

UnableToPlaceOrder = get_class('order.exceptions', 'UnableToPlaceOrder')


class PaymentDetailsView(CorePaymentDetailsView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentDetailsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        if self.preview:
            ctx['stripe_token_form'] = forms.StripeTokenForm(self.request.POST)
            ctx['order_total_incl_tax_cents'] = (
                    ctx['order_total'].incl_tax * 100
            ).to_integral_value()
        else:
            ctx['order_total_incl_tax_cents'] = (
                    ctx['order_total'].incl_tax * 100
            ).to_integral_value()
            ctx['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY

        return ctx

    def handle_first_order(self):

        try:
            user=self.request.user
            referal_obj = Referrals.objects.get(user=user, status=False)
            referrer = referal_obj.referred_by
            referralcoupon = ReferalVoucher.objects.get(id=2)
            referee_voucher = referralcoupon.referee_voucher
            voucher = referralcoupon.voucher
            referrer_baskets = referrer.baskets.all()

            user_voucher = UserVouchers.objects.get(voucher=voucher,
                                                    user=user, currently_used=True)

            user_voucher.redeemed = True
            user_voucher.redeemed_on = timezone.now()
            user_voucher.redeemed_count = 1
            user_voucher.currently_used = False
            user_voucher.save()

            referal_obj.status = True
            referal_obj.save()
            if referrer_baskets:
                basket = referrer_baskets.last()
                basket.vouchers.add(referee_voucher)
                Applicator().apply(basket, self.request.user,
                                   self.request)
                basket_vouchers = basket.vouchers.all()

        except:

            pass

    def handle_payment(self, order_number, total, **kwargs):

        stripe_token = self.request.POST['stripeToken']
        user_email = self.request.user.email
        customer = Facade().create_customer(user_email, stripe_token)

        stripe_ref = Facade().charge_with_customer(
            order_number,
            total,
            customer=customer,
            description=self.payment_description(order_number, total, **kwargs),
            metadata=self.payment_metadata(order_number, total, **kwargs))

        source_type, __ = SourceType.objects.get_or_create(name=PAYMENT_METHOD_STRIPE)
        source = Source(
            source_type=source_type,
            currency=settings.STRIPE_CURRENCY,
            amount_allocated=total.incl_tax,
            amount_debited=total.incl_tax,
            reference=stripe_ref)

        self.add_payment_source(source)
        self.add_payment_event(PAYMENT_EVENT_PURCHASE, total.incl_tax)

        if not Order.objects.filter(user=self.request.user, is_first_order=True).exists():
            self.handle_first_order()

    def payment_description(self, order_number, total, **kwargs):
        return self.request.POST[STRIPE_EMAIL]

    def payment_metadata(self, order_number, total, **kwargs):
        return {'order_number': order_number}
