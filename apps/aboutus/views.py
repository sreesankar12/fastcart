from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from oscar.core.loading import get_class, get_model
from .models import FaqModel, TermsModel


class FaqView(View):

    def get(self, request, *args, **kwargs):
        faq = FaqModel.objects.order_by("updated_at")
        context = {
            "faq": faq
        }
        return render(request, "aboutus/faq.html", context)


class TermsView(View):

    def get(self, request, *args, **kwargs):
        terms = TermsModel.objects.last()
        context = {
            "terms": terms
        }
        return render(request, "newtemp/terms.html", context)
