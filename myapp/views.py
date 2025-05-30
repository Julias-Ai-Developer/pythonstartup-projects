from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Record
from django.utils import timezone


@login_required
def dashboard(request):
    return render(request, "myapp/dashboard.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "dashboard")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "myapp/login.html")


def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get("firstName", "").strip()
        last_name = request.POST.get("lastName", "").strip()
        username = request.POST.get("userName", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        # Basic Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "myapp/signup.html")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return render(request, "myapp/signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "An account with this email already exists")
            return render(request, "myapp/signup.html")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")

    return render(request, "myapp/signup.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def forgotpassword_view(request):
    return render(request, "myapp/forgotpassword.html")


# add record
@login_required
def records_view(request):
    return render(request, "myapp/records.html")


@login_required
def add_records_view(request):
    if request.method == "POST":
        title = request.POST.get('recordTitle')
        category = request.POST.get('recordCategory')
        description = request.POST.get('recordDescription', '')
        date = request.POST.get("recordDate")
        status = request.POST.get('recordStatus', 'active')

        Record.objects.create(
            title=title,
            description=description,
            category=category,
            date=date,
            status=status,
            created_by=request.user
        )

        return redirect('add-records')  # redirect after POST

    # Only for GET request, fetch records and show page
    records = Record.objects.filter(created_by=request.user).order_by('-date')
    return render(request, "myapp/add-records.html", {"records": records})
