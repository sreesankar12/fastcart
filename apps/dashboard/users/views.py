from oscar.core.compat import get_user_model
from django.views.generic import (
    DeleteView, DetailView, FormView, ListView, UpdateView)

from apps.voucher.models import UserVouchers

User = get_user_model()


class UserDetailView(DetailView):
    template_name = 'oscar/dashboard/users/detail.html'
    model = User
    context_object_name = 'customer'

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     user_vouchers = UserVouchers.objects.get(user=customer)
    #     ctx['vouchers'] = user_vouchers
    #     return ctx
