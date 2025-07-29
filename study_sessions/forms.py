from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Sessions

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SessionsForm(forms.ModelForm):
    class Meta:
        model = Sessions
        fields = ['subject', 'duration', 'date', 'notes']
        