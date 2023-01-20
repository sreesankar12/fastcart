from django.db import models
from django.db.models import Sum
from oscar.apps.voucher.abstract_models import AbstractVoucher
from oscar.core.compat import get_user_model
from django.utils.translation import ugettext_lazy as _
from social_core.utils import user_is_authenticated
from solo.models import SingletonModel
from apps.customer.models import UserInvitation

# def normalize_fraction(d):
#     normalized = d.normalize()
#     sign, digit, exponent = normalized.as_tuple()
#     return normalized if exponent <= 0 else normalized.quantize(1)
#
#
User = get_user_model()
#
VOUCHER_TYPE_REFERRAL = 'referral'
VOUCHER_TYPE_FIRSTORDER = 'firstorder'

#
VOUCHER_TYPES = (
    (VOUCHER_TYPE_REFERRAL, 'Referral'),
    (VOUCHER_TYPE_FIRSTORDER, 'First Order'),
)


class Voucher(AbstractVoucher):
    pass


class UserVouchers(models.Model):
    """
    Model of vouchers allocated for each user.
    """

    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name='user_voucher')
    user = models.ForeignKey(User, related_name='user_vouchers', on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=VOUCHER_TYPES, default=VOUCHER_TYPE_REFERRAL)
    currently_used = models.BooleanField(default=False)
    redeemed = models.BooleanField(default=False)
    redeemed_on = models.DateTimeField(null=True, blank=True)
    redeemed_count = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        verbose_name = _('User Voucher')
        verbose_name_plural = _('User Vouchers')
        ordering = ['-currently_used']

    def __str__(self):
        return "%s - %s" % (self.user, self.voucher)


class ReferalVoucher(models.Model):

    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    referee_voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name='referee_voucher', null=True,
                                        blank=True)


from oscar.apps.voucher.models import *  # noqa isort:skip
