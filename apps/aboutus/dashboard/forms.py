from django import forms
from django.utils.translation import gettext_lazy as _
from oscar.core.loading import get_model
from apps.aboutus.models import FaqModel, TermsModel
# Aboutus = get_model('aboutus', 'AboutUsModel')


class FaqForm(forms.ModelForm):

    class Meta:
        model = FaqModel
        fields = ('title', 'description',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add faq question ',
                                            'width': '200px'}),
        }

    def __init__(self, *args, **kwargs):
        super(FaqForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['cols'] = 10
