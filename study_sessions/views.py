from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView, FormView)
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
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
    
# List, Filter, Pagination
class SessionListView(LoginRequiredMixin, ListView):
    model = Sessions
    template_name = 'study_sessions/sessions_list.html'
    context_object_name = 'sessions'
    paginate_by = 5

    def get_queryset(self):
        qs = Sessions.objects.filter(user=self.request.user)
        subject = self.request.GET.get("subject")
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        if subject:
            qs = qs.filter(subject__icontains=subject)
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        return qs