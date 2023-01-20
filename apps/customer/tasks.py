from time import sleep

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from celery import shared_task
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages

from apps.customer.tokens import account_activation_token
from fastcart import settings
from django.utils.encoding import force_bytes


@shared_task()
def send_registration_email_task(self, user):
    print("celery task mail")
    current_site = get_current_site(self.request)
    subject = 'Welcome to Fastcart!,Verify your Account.'
    message = render_to_string('user/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user_id': user.email,
        'token': account_activation_token.make_token(user),
    })
    recipient = user.email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
