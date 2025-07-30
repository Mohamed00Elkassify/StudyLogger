from django.urls import path
from .views import (RegisterView, SessionListView, SessionCreateView,
                     SessionDeleteView, SessionUpdateView, WeeklySummaryView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', SessionListView.as_view(), name='sessions_list'),
    path('add/', SessionCreateView.as_view(), name='sessions_add'),
    path('<int:pk>/edit/', SessionUpdateView.as_view(), name='sessions_edit'),
    path('<int:pk>/delete/', SessionDeleteView.as_view(), name='sessions_delete'),
    path('weekly-summary/', WeeklySummaryView.as_view(), name='weekly_summary'),

]