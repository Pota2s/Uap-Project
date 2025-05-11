from django.shortcuts import render
from django.http import HttpResponse,Http404
from hashlib import sha256
from .models import User,Product

def index(request):
    products_list : list[Product] = Product.objects.order_by("-product_name")
    ctx : dict[any : any] = dict()
    ctx[products_list] = products_list
    print(products_list)
    return render(request=request,template_name='home/index.html',context=ctx)

def users(request):
    user_list : list[User] = User.objects.order_by("-user_name")
    context : dict[any : any] = dict()
    context['user_list'] = user_list
    return render(request=request,template_name='home/users.html',context=context)

def userPage(request,user_id : int):
    
    context = dict()
    try:
        user : User = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    context['user'] = user


    return render(request=request,template_name='home/user.html',context=context)

def register(request):
    return HttpResponse("Registration methods here, it should ask for input directly on the page and create a user with the details provided.")

def login(request):
    return HttpResponse("Login method here, it should ask for input, then validate the user using SHA256 for the password")

