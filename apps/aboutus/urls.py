from django.contrib.flatpages import views
from django.urls import include, path

from apps.aboutus.dashboard.views import FaqCreateView

urlpatterns = [

    # path('add-faq', FaqCreateView.as_view(), name="faq-create"),
    path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
    path('license/', views.flatpage, {'url': '/license/'}, name='license'),
]