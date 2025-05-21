from django.urls import path

from .views import SignUpView,UserView
from .forms import CustomUserCreationForm 

urlpatterns = [
    path("signup/", SignUpView.as_view(form_class=CustomUserCreationForm), name="signup"),
    path("<int:user_id>/", UserView, name="user"),
]