from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from store.models import WishList,LibraryItem
from .models import CustomUser
from .forms import CustomUserChangeForm,AddFundsForm


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def user_view(request : HttpRequest, user_id : int):
    context = dict()
    context['user'] = CustomUser.objects.get(id=user_id)
    context['wishlist'] = list(WishList.objects.filter(user=context['user']))
    context['library'] = list(LibraryItem.objects.filter(user=context['user']))
    return render(request=request,template_name='accounts/user.html',context=context)

def logout_view(request : HttpRequest):
    context = dict()
    context['user'] = request.user
    return render(request=request,template_name='accounts/logout_confirmation.html',context=context)

def userhome_view(request : HttpRequest):
    context = dict()
    context['user'] = request.user
    context['wishlist'] = list(WishList.objects.filter(user=request.user))
    context['library'] = list(LibraryItem.objects.filter(user=request.user))
    return render(request=request,template_name='accounts/user_home.html',context=context)

def user_edit_view(request : HttpRequest):
    context = dict()
    context['user'] = request.user
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_home')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context['form'] = form
    return render(request=request,template_name='accounts/user_edit.html',context=context)

def add_funds_view(request : HttpRequest):
    context = dict()
    context['user'] = request.user
    if request.method == "POST":
        form = AddFundsForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            context['user'].wallet += amount # type: ignore
            context['user'].save()
            return redirect('user_home')
    else:
        form = AddFundsForm()
    context['form'] = form
    return render(request=request,template_name='accounts/add_funds.html',context=context)