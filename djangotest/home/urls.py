from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/<int:user_id>/",views.userPage,name="User page"),
    path("users/register/",views.register,name="Register"),
    path("users/login/",views.login,name="Login")
]
