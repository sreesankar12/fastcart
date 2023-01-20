import logging
from django.contrib import messages

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode

from oscar.apps.customer.signals import user_registered
from oscar.core.compat import get_user_model
from oscar.core.loading import get_class, get_model

from apps.customer.tasks import send_registration_email_task
from apps.customer.tokens import account_activation_token
from django.utils.encoding import force_bytes

User = get_user_model()
CommunicationEventType = get_model('communication', 'CommunicationEventType')
CustomerDispatcher = get_class('customer.utils', 'CustomerDispatcher')

logger = logging.getLogger('oscar.customer')


class PageTitleMixin(object):
    """
    Passes page_title and active_tab into context, which makes it quite useful
    for the accounts views.

    Dynamic page titles are possible by overriding get_page_title.
    """
    page_title = None
    active_tab = None

    # Use a method that can be overridden and customised
    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('page_title', self.get_page_title())
        ctx.setdefault('active_tab', self.active_tab)
        return ctx


class RegisterUserMixin(object):
    communication_type_code = 'REGISTRATION'

    def register_user(self, form):
        """
        Create a user instance and send a new registration email (if configured
        to).
        """
        user = form.save()
        user.is_active = False
        user.save()

        self.send_registration_email(user)
        # Raise signal robustly (we don't want exceptions to crash the request
        # handling).
        user_registered.send_robust(
            sender=self, request=self.request, user=user)

        # We have to authenticate before login
        try:
            user = authenticate(
                username=user.email,
                password=form.cleaned_data['password1'])
        except User.MultipleObjectsReturned:
            # Handle race condition where the registration request is made
            # multiple times in quick succession.  This leads to both requests
            # passing the uniqueness check and creating users (as the first one
            # hasn't committed when the second one runs the check).  We retain
            # the first one and deactivate the dupes.
            logger.warning(
                'Multiple users with identical email address and password'
                'were found. Marking all but one as not active.')
            # As this section explicitly deals with the form being submitted
            # twice, this is about the only place in Oscar where we don't
            # ignore capitalisation when looking up an email address.
            # We might otherwise accidentally mark unrelated users as inactive
            users = User.objects.filter(email=user.email)
            user = users[0]
            for u in users[1:]:
                u.is_active = False
                u.save()

        # auth_login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        return user

    def send_registration_email(self, user):
        send_registration_email_task(self, user)

    # def send_registration_email(self, user):
    #     current_site = get_current_site(self.request)
    #     subject = 'Welcome to Fastcart!,Verify your Account.'
    #     message = render_to_string('user/acc_active_email.html', {
    #         'user': user,
    #         'domain': current_site.domain,
    #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #         'user_id': user.email,
    #         'token': account_activation_token.make_token(user),
    #     })
    #     recipient = user.email
    #     send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
    #     messages.success(self.request, "An email has been send to you for account activation.")
