from urllib.request import urlopen
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount import app_settings
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.utils import user_email

from oscar.core.compat import get_user_model
from apps.customer.models import Referrals, UserInvitation
# from utils.helpers import create_user
from apps.voucher.models import UserVouchers, ReferalVoucher, VOUCHER_TYPE_REFERRAL

User = get_user_model()


class FastcartAdapter(DefaultAccountAdapter):
    """
    function called to generate user's username when signup using allauth
    """
    def generate_unique_username(self, txts, regex=None):
        # return the users email as username
        return txts[2]


class FastcartMySocialAdapter(DefaultSocialAccountAdapter):

    def is_auto_signup_allowed(self, request, sociallogin):
        auto_signup = app_settings.AUTO_SIGNUP
        if auto_signup:
            email = user_email(sociallogin.user)
            if email:
                # code here is intentionally removed to login automatically if the the account already exists.
                pass
            elif app_settings.EMAIL_REQUIRED:
                auto_signup = False
        return auto_signup

    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if not user.email:
            user.delete()
            response = redirect(reverse('customer:login'))
            messages.error(request, 'Your account has no email address associated with it.')
            raise ImmediateHttpResponse(response)
        if user.id:
            return
        # Saves the user photo.
        try:

            user.save()
        except Exception as e:
            print(e, '############')
        # If user exists, connect the account to the existing account and login
        try:
            customer = User.objects.get(email=user.email)
            sociallogin.connect(request, customer)
            user_email(request, customer, 'none')
        except User.DoesNotExist:
            pass
        # Add new referrals entry if any referrer is present in session
        if 'fastcart-refercode' in request.session:
            try:
                """
                if registered user is a referred user create a referral obj and add referral coupon to the referee.
                """
                referrer_obj = UserInvitation.objects.get(invite_code=request.session['fastcart-refercode'])
                referrer = referrer_obj.user
                referal_obj = Referrals.objects.create(user=user, referred_by=referrer)
                del request.session['fastcart-refercode']
                referralcoupon = ReferalVoucher.objects.get(id=2)
                referee_voucher = referralcoupon.referee_voucher
                referervoucher = UserVouchers.objects.create(voucher=referee_voucher,
                                                             user=referrer, type=VOUCHER_TYPE_REFERRAL,
                                                             currently_used=True)
            except Exception as e:
                print(e)
