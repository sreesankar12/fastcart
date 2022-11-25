from django.conf import settings
from oscar.apps.payment.exceptions import UnableToTakePayment, InvalidGatewayRequestError

import stripe
from stripe.error import CardError, InvalidRequestError


class Facade(object):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    @staticmethod
    def get_friendly_decline_message(error):
        return 'The transaction was declined by your bank - please check your bankcard details and try again'

    @staticmethod
    def get_friendly_error_message(error):
        return 'An error occurred when communicating with the payment gateway.'

    def charge(self, order_number, total, card, currency=settings.STRIPE_CURRENCY, description=None,
               metadata=None, **kwargs):
        print("----------------------------------------------------")
        print(order_number, total, "card >", card, "<card ", settings.STRIPE_CURRENCY)
        print("----------------------------------------------------")
        # print(total.incl_tax * 100).to_integral_value())
        try:
            return stripe.PaymentIntent.create(
                amount=(total.incl_tax * 100).to_integral_value(),
                currency=currency,
                card=card,
                description=description,
                metadata=(metadata or {'order_number': order_number}),
                **kwargs)
        except stripe.error.CardError as e:
            raise UnableToTakePayment(self.get_friendly_decline_message(e))
        except stripe.error.StripeError as e:
            raise InvalidGatewayRequestError(self.get_friendly_error_message(e))

    def charge_with_customer(self, order_number, total, customer, currency="inr",
                             description=None, metadata=None, **kwargs):
        try:
            return stripe.PaymentIntent.create(
                amount=(total.incl_tax * 100).to_integral_value(),
                currency=currency,
                customer=customer,
                description=description,
                metadata=(metadata or {'order_number': order_number}),
                **kwargs)
        except stripe.error.CardError as e:
            raise UnableToTakePayment(self.get_friendly_decline_message(e))
        except stripe.error.StripeError as e:
            raise InvalidGatewayRequestError(self.get_friendly_error_message(e))

    def create_customer(self, email, token):
        try:
            return stripe.Customer.create(
                email=email,
                source=token,
            )

        except stripe.error.StripeError as e:
            raise UnableToTakePayment(self.get_friendly_decline_message(e))
    #
    # def retrieve_source(self, id, card_token):
    #     try:
    #         return stripe.Customer.retrieve_source(id, card_token)
    #     except stripe.error.StripeError as e:
    #         raise InvalidGatewayRequestError(self.get_friendly_error_message(e))
