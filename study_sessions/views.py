from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView)
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from datetime import date, timedelta
from .models import Session
from .forms import RegisterForm, SessionsForm
from django.db.models import Sum


# Create your views here.

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/signup'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
#* List, Filter, Pagination
class SessionListView(LoginRequiredMixin, ListView):
    model = Session
    template_name = 'study_sessions/sessions_list.html'
    context_object_name = 'sessions'
    paginate_by = 5

    def get_queryset(self):
        qs = Session.objects.filter(user=self.request.user)
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

#* create
class SessionCreateView(LoginRequiredMixin, CreateView):
    model = Session
    form_class = SessionsForm
    template_name = 'study_sessions/sessions_form.html'
    success_url = reverse_lazy('sessions_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#* update
class SessionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Session
    form_class = SessionsForm
    template_name = 'study_sessions/sessions_form.html'
    success_url = reverse_lazy('sessions_list')

    def test_func(self):
        return Session.objects.filter(
            id=self.kwargs['pk'], user=self.request.user
        ).exists()

#* delete
class SessionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Session
    template_name = 'study_sessions/sessions_confirm_delete.html'
    success_url = reverse_lazy('sessions_list')

    def test_func(self):
        return Session.objects.filter(
            id=self.kwargs['pk'], user=self.request.user
        ).exists()
    
#* Weekly Summary
class WeeklySummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'study_sessions/weekly_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        startweek = today - timedelta(days=today.weekday())
        endweek = startweek + timedelta(days=6)
        sessions = Session.objects.filter(
            user=self.request.user,
            date__range=(startweek, endweek)
        )
        summary = sessions.values('subject').annotate(total=Sum('duration'))
        context['summary'] = summary
        return context