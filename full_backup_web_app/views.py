from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
# from .models import Customers, Products, Suppliers, Entry_notes
# from .forms import CustomerForm, ProductsForm, SuppliersForm, Entry_notesForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

import subprocess
import time
import platform
import os

# Library for the GUI
from tkinter import *
from tkinter import filedialog


# Create your views here.

# view for the login template
def auth_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bem vindo ao Full Backup, {username.capitalize()}")
            return redirect("home")
        else:
            messages.error(request, "Nome de usuário ou senha incorretos!")
    return render(request, "auth/login.html")

# View for the home page after login (to be developed)
def home(request):
    if request.user.is_authenticated:
        return render(request, "auth/home.html")
    else:
        messages.error(request, "Você deve estar logado para obter acesso ao Full Backup!")
        return redirect("login")
    
# Logout function
@login_required
def auth_logout(request):
    logout(request)
    messages.info(request, "Logout bem-sucedido")
    return redirect("login")
    
#View for the signup template
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confpass = request.POST.get("confpass")
        if password != confpass:
            messages.error(request, "Sua senha e confirmação não conferem!")
        else:
            my_user = User.objects.create_user(username, email, password)
            my_user.save()
            my_user.clean_fields()
            messages.success(request, f"Usuário: {my_user.username} criado com êxito!")
            # send_email(username, email)
            return redirect("login")
    return render(request, "auth/signup.html")


# This function acknowledges which OS the program is running on
def select_os():
    os = platform.system()
    return os

def source_dir_func(response):
    source_dir = filedialog.askdirectory()
    #source_dir = os.getcwd()
    return JsonResponse({'source': source_dir})



def dest_dir_func(response):
    dest_dir = filedialog.askdirectory()
    #dest_dir = os.getcwd()
    return JsonResponse({'destination': dest_dir})