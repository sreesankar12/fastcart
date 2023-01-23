from django.contrib import admin
from .models import FaqModel,TermsModel
# Register your models here.
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _
from django.db import models
from ckeditor.widgets import CKEditorWidget


class AboutUsAdmin(admin.ModelAdmin):
    pass


admin.site.register(FaqModel, AboutUsAdmin)
admin.site.register(TermsModel)


class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }


# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
