from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Superadmin, Record, Category, Event
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import secrets
import string
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# import json

# PDF template
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
import io


# users to login not as superadmin
from django.contrib.auth.models import Group


# DRF API view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EventSerializer


class EventListAPI(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


@login_required
def dashboard(request):
    if not (request.user.is_superuser or request.user.role == "SuperSystemAdmin"):
        messages.error(request, "You do not have permission to access this page.")
        # or another page if preferred

    count = Superadmin.objects.filter(role="SuperAdmin").count()
    total_records = Record.objects.count()

    records = Record.objects.filter(created_by=request.user).order_by("-updated_at")

    return render(
        request,
        "myapp/dashboard.html",
        {"records": records, "superadmin_count": count, "total_records": total_records},
    )


#authentication views only


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            superadmin_obj = Superadmin.objects.get(email=email)
            user = authenticate(
                request, username=superadmin_obj.username, password=password
            )
        except Superadmin.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "dashboard")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "myapp/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def forgotpassword_view(request):
    return render(request, "myapp/forgotpassword.html")


@login_required
def records_view(request):
    records = Record.objects.filter(created_by=request.user).order_by("-updated_at")
    return render(request, "myapp/records.html", {"records": records})


@login_required
def add_records_view(request):
    if request.method == "POST":
        title = request.POST.get("recordTitle")
        category = request.POST.get("recordCategory")
        description = request.POST.get("recordDescription", "")

        Record.objects.create(
            title=title,
            description=description,
            category=category,
            created_by=request.user,
        )
        return redirect("add-records")

    records = Record.objects.filter(created_by=request.user).order_by("-updated_at")
    categories = Category.objects.all()

    return render(
        request,
        "myapp/add-records.html",
        {"records": records, "categories": categories},
    )


# edit/update


@login_required
def categories_view(request):
    if request.method == "POST":
        category_name = request.POST.get("categoryName")

        if category_name:
            Category.objects.create(
                category_name=category_name,
                created_by=request.user,
            )
            return redirect("categories")

    categories = Category.objects.filter(created_by=request.user).order_by(
        "-id"
    )
    return render(request, "myapp/categories.html", {"categories": categories})


@login_required
def reports_view(request):
    categories = Category.objects.filter(created_by=request.user)
    records = Record.objects.filter(created_by=request.user).order_by("-updated_at")
    return render(
        request, "myapp/reports.html", {"categories": categories, "records": records}
    )


@login_required
def profile_view(request):
    return render(request, "myapp/profile.html")





#changePassword

@login_required
def edit_password(request):
    #"""Handle password change"""
    if request.method == "POST":
        new_password = request.POST.get("newPassword")
        confirm_password = request.POST.get("confirmPassword")
        
        if not new_password:
            messages.error(request, "Password Cannot Be Empty")
        elif len(new_password) < 8:  # Add minimum length validation
            messages.error(request, "Password must be at least 8 characters long")
        elif new_password != confirm_password:
            messages.error(request, "Passwords do not match, try again")
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "Password updated successfully. Please log in again.")
            return redirect("login")
    
    # Redirect back to profile page if there are errors or for GET requests
    return redirect("profile")












@login_required
def settings_view(request):
    return render(request, "myapp/settings.html")


@login_required
def analytics_view(request):
    return render(request, "myapp/analytics.html")


@login_required
def schedules_view(request):
    return render(request, "myapp/schedules.html")


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password

@login_required
def business_view(request):
    # Only allow Super System Admin (full control) to access
    if not (request.user.is_superuser or request.user.role == "SuperSystemAdmin"):
        messages.error(request, "You do not have permission to access this page.")
        return redirect("dashboard")

    if request.method == "POST":
        first_name = request.POST.get("adminFirstname")
        last_name = request.POST.get("adminLastname")
        email = request.POST.get("adminEmail")
        password = generate_random_password()
        company = request.POST.get("companyName")
        phone = request.POST.get("phoneNumber")

        if not all([first_name, last_name, email, password, company, phone]):
            messages.error(request, "Please fill in all fields.")
            return render(request, "myapp/business.html")

        User = Superadmin
        if User.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists.")
            return render(request, "myapp/business.html")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            company=company,
            phone_number=phone,
            is_staff=True,
            is_superuser=False,
        )

        try:
            limited_group = Group.objects.get(name="LimitedAdmin")
            user.groups.add(limited_group)
        except Group.DoesNotExist:
            pass

        user.save()

        # Email context
        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'company': company,
        }

        html_content = render_to_string('myapp/business_email.html', context)
        text_content = "You have been registered on RecordLite. Please view this email in an HTML-compatible email client."

        msg = EmailMultiAlternatives(
            subject="Welcome to RecordLite App",
            body=text_content,
            from_email="RECORDLITE <muyambijulias@gmail.com>",
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        messages.success(
            request, f"Business admin user created. Temporary password: {password}"
        )
        return redirect("business")

    # GET: Display all Superadmin users with role called SuperAdmin
    users = Superadmin.objects.filter(role="SuperAdmin").order_by('-id')
    return render(request, "myapp/business.html", {"users": users})


# def business_email(request):
#     return render(request , "myapp/business_email.html")


@login_required
def business_users_view(request):
    return render(request, "myapp/business-users.html")





@login_required
def export_records_pdf(request):
    records = Record.objects.filter(created_by=request.user).order_by("-updated_at")
    template_path = "myapp/records_pdf.html"
    context = {"records": records, "superadmin": request.user}

    template = get_template(template_path)
    html = template.render(context)

    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="records_report.pdf"'
        return response
    return HttpResponse("Failed to generate PDF", status=500)


#chatbot

# @csrf_exempt
# def chatbot_response(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_input = data.get('message', '')

#         # Step 2 will go here later
#         return JsonResponse({'response': f"You said: {user_input}"})
#     else:
#         return JsonResponse({'error': 'POST method required'}, status=405)


