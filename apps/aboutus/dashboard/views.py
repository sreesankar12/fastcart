from django.shortcuts import render, redirect
from django.contrib import messages
from oscar.core.loading import get_class, get_model
from django.views.generic.edit import View, CreateView, UpdateView ,DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from apps.aboutus.dashboard.forms import FaqForm

FaqModel = get_model('aboutus', 'FaqModel')
Terms = get_model('aboutus', 'TermsModel')


class FaqCreateView(CreateView):
    model = FaqModel
    form_class = FaqForm

    def get_success_url(self):
        return reverse("aboutus-dashboard:faq-list")


class FaqListView(ListView):
    model = FaqModel


class FaqDetailView(DetailView):
    model = FaqModel


class FaqUpdateView(UpdateView):
    model = FaqModel

    fields = [
        "title",
        "description"
    ]

    def get_success_url(self):
        return reverse("aboutus-dashboard:faq-list")


class FaqDeleteView(DeleteView):
    # specify the model you want to use
    model = FaqModel

    def get_success_url(self):
        return reverse("aboutus-dashboard:faq-list")



