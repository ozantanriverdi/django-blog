'''Import render function to show html pages
Import RegisterForm to create register forms in register.html'''
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db import IntegrityError
from .forms import RegisterForm, LoginForm
# Create your views here.


def register(request):
    '''User Register Function'''
    form = RegisterForm(request.POST or None)
    # if request.method == "GET" -> request.POST is empty and empty form
    # created, if request.method == "GET" -> can't get into if below

    try:
        if form.is_valid():
            # uses the 'clean' function of RegisterForm
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # The get() method returns the value of the item with the
            # specified key from the values dictionary.'''

            newUser = User(username=username)
            newUser.set_password(password)

            newUser.save()
            login(request, newUser)
            messages.info(request, "Registered Successfully!")
            return redirect("index")
        context = {
            "form": form
        }
        return render(request, "register.html", context)
    except IntegrityError:
        # Check if username is unique
        messages.warning(request, "Username taken already!")
        return redirect("index")


def loginUser(request):
    '''User Login function'''
    form = LoginForm(request.POST or None)

    context = {
        "form": form
    }

    if form.is_valid():
        # No overwritten clean method -> makes simple checks like
        # making sure all fields have been filled
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            # No match in database
            messages.info(request, "Invalid Username or Password!")
            return render(request, "login.html", context)

        messages.success(request, "Login Successful!")
        login(request, user)

        return redirect("index")
    return render(request, "login.html", context)


def logoutUser(request):
    '''User Logout function'''
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect("index")
