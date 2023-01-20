from django.db import models
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
# Create your models here.


class FaqModel(models.Model):
    title = models.TextField(max_length=500)
    description = RichTextField()
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'aboutus'

    def __str__(self):
        return self.title


class TermsModel(models.Model):
    terms = RichTextField()
    updated_at = models.DateTimeField(auto_now_add=True)

