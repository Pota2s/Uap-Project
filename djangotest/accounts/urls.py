from django.urls import path

from .views import SignUpView,user_view, logout_view,userhome_view, user_edit_view, add_funds_view
from .forms import CustomUserCreationForm 

urlpatterns = [
    path("signup/", SignUpView.as_view(form_class=CustomUserCreationForm), name="signup"),
    path("logout/confirmation/", logout_view, name="logout_confirmation"),
    path("", userhome_view, name="user_home"),
    path("edit/", user_edit_view, name="user_edit"),
    path("<int:user_id>/", user_view, name="user"),
    path("addfunds/", add_funds_view, name="add_funds"),
]