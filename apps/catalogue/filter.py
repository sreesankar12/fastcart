import django_filters
from oscar.core.loading import get_class, get_model
from django import forms

Product = get_model('catalogue', 'product')


class ProductPriceFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields= ('id', 'title','images')
