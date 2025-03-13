from django.shortcuts import render
from django.http import HttpResponse
from hashlib import sha256
from .models import User

def index(request):
    return HttpResponse("Hello, world. You're at the home index.")

def register(request):
    return HttpResponse("Registration methods here, it should ask for input directly on the page and create a user with the details provided.")

def login(request):
    return HttpResponse("Login method here, it should ask for input, then validate the user using SHA256 for the password")

