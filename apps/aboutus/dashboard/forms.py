from django import forms
from django.utils.translation import gettext_lazy as _
from oscar.core.loading import get_model
from apps.aboutus.models import AboutUsModel,TermsModel
# Aboutus = get_model('aboutus', 'AboutUsModel')


class DashboardAboutusUpdateForm(forms.ModelForm):
    class Meta:
        model = AboutUsModel
        fields = ('description',)


class DashboardTermsUpdateForm(forms.ModelForm):
    class Meta:
        model = TermsModel
        fields = ('terms',)

