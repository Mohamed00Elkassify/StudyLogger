from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView, FormView)
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import Sessions
from .forms import RegisterForm, SessionsForm


# Create your views here.
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/signup'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)