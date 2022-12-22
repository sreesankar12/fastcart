from django.contrib import admin
from .models import AboutUsModel,TermsModel
# Register your models here.


class AboutUsAdmin(admin.ModelAdmin):
    pass


admin.site.register(AboutUsModel, AboutUsAdmin)
admin.site.register(TermsModel)
