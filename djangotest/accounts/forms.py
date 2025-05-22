from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm # type: ignore
from django import forms
from .models import CustomUser

class CustomUserCreationForm(AdminUserCreationForm):
    pass
# Register your models here.
    class Meta:
        model = CustomUser
        fields = ("username","email")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username","email")

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