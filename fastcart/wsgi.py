"""
WSGI config for fastcart project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
# import whitenoise
from django.core.wsgi import get_wsgi_application

# from whitenoise.django import DjangoWhiteNoise
#   application = DjangoWhiteNoise(application)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastcart.settings')

application = get_wsgi_application()
