from django.shortcuts import render
from django.contrib import messages
from oscar.core.loading import get_class, get_model
from django.views.generic.edit import View
from.forms import DashboardAboutusUpdateForm,DashboardTermsUpdateForm

Aboutus = get_model('aboutus', 'AboutUsModel')
Terms = get_model('aboutus', 'TermsModel')


class DashboardAboutusUpdateView(View):
    def get(self, request):
        if Aboutus.objects.exists():
            obj = Aboutus.objects.last()
            form = DashboardAboutusUpdateForm(instance=obj)
        else:
            form = DashboardAboutusUpdateForm
        context = {
            "form": form
        }
        return render(request, "dashboard/aboutus/aboutus_update.html", context)

    def post(self, request):
        form = DashboardAboutusUpdateForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            form.save()
            messages.success(request,"Changes Saved")
        return render(request, "dashboard/aboutus/aboutus_update.html", context)


class DashboardTermsUpdateView(View):
    def get(self, request):
        if Terms.objects.exists():
            obj = Terms.objects.last()
            form = DashboardTermsUpdateForm(instance=obj)
        else:
            form = DashboardTermsUpdateForm
        context = {
            "form": form
        }
        return render(request, "dashboard/aboutus/terms_update.html", context)

    def post(self, request):
        form = DashboardTermsUpdateForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            form.save()
            messages.success(request, "Changes Saved")
        return render(request, "dashboard/aboutus/terms_update.html", context)

