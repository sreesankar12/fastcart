from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from oscar.core.loading import get_class, get_model
from.models import AboutUsModel,TermsModel


class AboutUsView(View):

    def get(self, request, *args, **kwargs):
        aboutus= AboutUsModel.objects.last()
        context = {
            "aboutus": aboutus
        }
        return render(request, "newtemp/about_us.html", context)


class TermsView(View):

    def get(self, request, *args, **kwargs):
        terms = TermsModel.objects.last()
        context = {
            "terms": terms
        }
        return render(request, "newtemp/terms.html", context)
