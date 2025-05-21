from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from store.models import WishList


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def UserView(request : HttpRequest, user_id : int):
    context = dict()
    context['user'] = request.user
    context['wishlist'] = list(WishList.objects.filter(user=request.user))
    return render(request=request,template_name='accounts/user.html',context=context)
