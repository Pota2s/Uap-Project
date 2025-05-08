from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/<int:user_id>/",views.userPage,name="User page")
]
