"""fastcart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from django.apps import apps
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),

    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.

    path('admin/', admin.site.urls),

    path('', include(apps.get_app_config('oscar').urls[0])),
    path("auth_accounts/", include("allauth.urls")),
    path('pages/', apps.get_app_config('aboutus').urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('dashboard/aboutus/', apps.get_app_config('aboutus_dashboard').urls),
    path('pages/', include('django.contrib.flatpages.urls')),

    # url(r'^weblog/', include('zinnia.urls')),
    # url(r'^comments/', include('django_comments.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
