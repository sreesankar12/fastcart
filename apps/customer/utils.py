from oscar.core.loading import get_class
from apps.voucher.models import VOUCHER_TYPE_FIRSTORDER

from oscar.core.loading import (
    get_class, get_classes, get_model, get_profile_class)

Applicator = get_class('offer.utils', 'Applicator')


def apply_firstorder_voucher(request, voucher, user):

    "get basket for a user and apply first order voucher to basket"

    Basket = get_model('basket', 'Basket')

    try:
        basket, __ = Basket.objects.filter(status__in=["Open", "Saved"]).get_or_create(owner=user)
    except Basket.MultipleObjectsReturned:
        # Not sure quite how we end up here with multiple baskets.
        # We merge them and create a fresh one
        old_baskets = list(Basket.objects.filter(status__in=["Open", "Saved"]).filter(owner=user))
        basket = old_baskets[0]
        for other_basket in old_baskets[1:]:
            basket.merge(other_basket, add_quantities=False)

    request.basket = basket
    print("id of basket:", basket.id)
    basket.vouchers.clear()
    basket.vouchers.add(voucher)
    Applicator().apply(basket, request.user,
                       request)
    basket_vouchers = basket.vouchers.all()
    print(basket_vouchers)


def get_voucher(user, basket=None):

    user_vouchers = user.user_vouchers
    user_vouchers_count = user.user_vouchers.count()
    highest_voucher = None
    highest_discount = 0
    if user_vouchers_count > 0:
        for user_voucher in user_vouchers:
            if user_voucher.voucher.benefit.type == 'Percentage':
                discount = basket.total_incl_tax * (user_voucher.voucher.benefit.value / 100)
                if discount > highest_discount:
                    highest_discount = discount
                    highest_voucher = user_voucher.voucher
            else:
                discount = user_voucher.voucher.benefit.value
                if discount > highest_discount:
                    highest_discount = discount
                    highest_voucher = user_voucher.voucher
    print(highest_voucher)
    return highest_voucher


def apply_voucher_to_cart(basket, user=None, voucher=None):
    print("apply voucher fn")
    # if not basket.owner:
    #     basket.owner = user
    #     basket.save(update_fields=['owner'])
    # if user_voucher:
    #     voucher = user_voucher.voucher
    # elif user:
    #     voucher = get_voucher(user, basket)
    # else:
    #     voucher = get_voucher(basket.owner, basket)
    # # voucher = get_voucher(user) if user else get_voucher(basket.owner)
    # status, error_message = False, None
    voucher = voucher
    print(voucher)

    def add_voucher():
        if not voucher.is_expired() and voucher.is_active():
            basket.vouchers.clear()
            basket.vouchers.add(voucher)

    if voucher:
        basket_vouchers = basket.vouchers.all()

        if basket_vouchers.count() > 0:
            current_voucher = basket_vouchers[0]
            if not current_voucher.id == voucher.id:
                # basket.vouchers.clear()
                add_voucher()
        else:
            add_voucher()

        # Recalculate discounts to see if the voucher gives any
        Applicator().apply(basket, basket.owner)
        print("applied")

