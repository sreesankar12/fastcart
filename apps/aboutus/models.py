from django.db import models
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
# Create your models here.


class AboutUsModel(models.Model):
    title = models.CharField(max_length=500)
    description = RichTextField()
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'aboutus'


class TermsModel(models.Model):
    terms = RichTextField()
    updated_at = models.DateTimeField(auto_now_add=True)

