from django.shortcuts import render, redirect, get_object_or_404
# from .models import Customers, Products, Suppliers, Entry_notes
# from .forms import CustomerForm, ProductsForm, SuppliersForm, Entry_notesForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

# view for the login template
def auth_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome to Stock Control: {username}")
            return redirect("home")
        else:
            messages.error(request, "Username or password incorrect")
    return render(request, "auth/login.html")

# View for the home page after login (to be developed)
def home(request):
    if request.user.is_authenticated:
        return render(request, "auth/home.html")
    else:
        messages.error(request, "You must be logged in to grant access to Stock Control")
        return redirect("login")
    
# Logout function
@login_required
def auth_logout(request):
    logout(request)
    messages.info(request, "You have logged out successfully")
    return redirect("login")
    
#View for the signup template
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confpass = request.POST.get("confpass")
        if password != confpass:
            messages.error(request, "Your password and confirmation do not match")
        else:
            my_user = User.objects.create_user(username, email, password)
            my_user.save()
            my_user.clean_fields()
            messages.success(request, f"User: {my_user.username} successfully created")
            # send_email(username, email)
            return redirect("login")
    return render(request, "auth/signup.html")