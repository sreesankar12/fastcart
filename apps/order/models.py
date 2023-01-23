from oscar.apps.order.abstract_models import AbstractOrder
from django.db import models


class Order(AbstractOrder):

    is_first_order = models.BooleanField(default=False)











from oscar.apps.order.models import *  # noqa isort:skip
