from django.contrib import admin
from .models import Invitation, UserInvitation, Referrals
# Register your models here.

admin.site.register(Invitation)
admin.site.register(UserInvitation)
admin.site.register(Referrals)
