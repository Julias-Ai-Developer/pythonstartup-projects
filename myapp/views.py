from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Superadmin, Record, Category, Event
from django.utils import timezone

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
    records = Record.objects.filter(created_by=request.user).order_by("-date")
    return render(request, "myapp/dashboard.html", {"records": records, "superadmin_count": count})


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
    records = Record.objects.filter(created_by=request.user).order_by("-date")
    return render(request, "myapp/records.html", {"records": records})


@login_required
def add_records_view(request):
    if request.method == "POST":
        title = request.POST.get("recordTitle")
        category = request.POST.get("recordCategory")
        description = request.POST.get("recordDescription", "")
        date = request.POST.get("recordDate")
        status = request.POST.get("recordStatus", "active")

        Record.objects.create(
            title=title,
            description=description,
            category=category,
            date=date,
            status=status,
            created_by=request.user,
        )
        return redirect("add-records")

    records = Record.objects.filter(created_by=request.user).order_by("-date")
    categories = Category.objects.all()

    return render(
        request,
        "myapp/add-records.html",
        {"records": records, "categories": categories},
    )


@login_required
def categories_view(request):
    if request.method == "POST":
        category_name = request.POST.get("categoryName")
        category_date = request.POST.get("categoryDate")

        if category_name and category_date:
            Category.objects.create(
                category_name=category_name,
                category_date=category_date,
                created_by=request.user,
            )
            return redirect("categories")

    categories = Category.objects.filter(created_by=request.user).order_by(
        "-category_date"
    )
    return render(request, "myapp/categories.html", {"categories": categories})


@login_required
def reports_view(request):
    categories = Category.objects.filter(created_by=request.user)
    records = Record.objects.filter(created_by=request.user).order_by("-date")
    return render(
        request, "myapp/reports.html", {"categories": categories, "records": records}
    )


@login_required
def profile_view(request):
    return render(request, "myapp/profile.html")


@login_required
def settings_view(request):
    return render(request, "myapp/settings.html")


@login_required
def analytics_view(request):
    return render(request, "myapp/analytics.html")


@login_required
def schedules_view(request):
    return render(request, "myapp/schedules.html")


@login_required
def business_view(request):
    # Only allow Super System Admin (full control) to access
    if not (request.user.is_superuser or request.user.role == "SuperSystemAdmin"):
        messages.error(request, "You do not have permission to access this page.")
        return redirect("dashboard")  # or another safe page

    if request.method == "POST":
        first_name = request.POST.get("adminFirstname")
        last_name = request.POST.get("adminLastname")
        email = request.POST.get("adminEmail")
        password = request.POST.get("password")
        company = request.POST.get("companyName")
        phone = request.POST.get("phoneNumber")

        if not all([first_name, last_name, email, password, company, phone]):
            messages.error(request, "Please fill in all fields.")
            return render(request, "myapp/business.html")

        User = Superadmin  # your custom user model
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
        messages.success(request, "Business admin user created successfully.")
        return redirect("business")
    # GET: Display all Superadmin users with role called SuperAdmin
    users = Superadmin.objects.filter(role="SuperAdmin")

    return render(request, "myapp/business.html", {"users": users})


@login_required
def export_records_pdf(request):
    records = Record.objects.filter(created_by=request.user).order_by("-date")
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
