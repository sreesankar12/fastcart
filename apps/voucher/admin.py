from django.contrib import admin
from .models import ReferalVoucher, UserVouchers, Voucher


admin.site.register(ReferalVoucher)
admin.site.register(UserVouchers)
admin.site.register(Voucher)


