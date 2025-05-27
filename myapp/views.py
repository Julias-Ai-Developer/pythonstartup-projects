from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def home(request):
    return render(request, "myapp/home.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get(
            "username"
        )  # Or use 'email' if you change the auth system
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "home")  # Redirect to next or home
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "myapp/login.html")


def signup_view(request):
    return render(request, "myapp/signup.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def forgotpassword_view(request):
    return render(request, "myapp/forgotpassword.html")
