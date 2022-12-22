from django.contrib.flatpages import views
from django.urls import include, path


urlpatterns = [
    path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
    path('license/', views.flatpage, {'url': '/license/'}, name='license'),
]