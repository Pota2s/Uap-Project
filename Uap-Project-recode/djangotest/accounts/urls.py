from django.urls import path

from .views import SignUpView
from .forms import CustomUserCreationForm 

urlpatterns = [
    path("signup/", SignUpView.as_view(form_class=CustomUserCreationForm), name="signup"),
]