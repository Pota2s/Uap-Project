from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from .models import CustomUser

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'input-field'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'input-field'
        })
    )

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'input-field'}),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': ' ', 'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'placeholder': ' ', 'class': 'input-field'}),
        }


class AddFundsForm(forms.Form):
    amount = forms.FloatField(
        label="Amount",
        min_value=0.0,
        max_value=10000.0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter amount to add',
            'class': 'form-control'
        })
    )