from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import EventListAPI


urlpatterns = [
    path("", views.login_view, name="login"),  # dashboardpage
    path("dashboard/", views.dashboard, name="dashboard"),
    path("reports/", views.reports_view, name="reports"),
    path("profile/", views.profile_view, name="profile"),
    path("business/", views.business_view, name="business"),
    path("settings/", views.settings_view, name="settings"),
    path("analytics/", views.analytics_view, name="analytics"),
    path("schedules/", views.schedules_view, name="schedules"),
    path("categories/", views.categories_view, name="categories"),
    path("records/", views.records_view, name="records"),
    path("add-records/", views.add_records_view, name="add-records"),
    # PDF export
    path("export-pdf/", views.export_records_pdf, name="export_pdf"),
    # calendar
    path("api/events/", EventListAPI.as_view(), name="event-list-api"),
    # Auth
    path("login/", views.login_view, name="login"),
   
    path("logout/", views.logout_view, name="logout"),
    path("forgotpassword/", views.forgotpassword_view, name="forgotpassword"),
]

# ✅ Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
