from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views,category_views
from .views import EventListAPI


urlpatterns = [
    path("", views.login_view, name="login"),  # dashboardpage
    path("dashboard/", views.dashboard, name="dashboard"),
    path("reports/", views.reports_view, name="reports"),
    path("profile/", views.profile_view, name="profile"),
    path('edit_password/', views.edit_password, name='editPassword'),  # For password editing

    path("business/", views.business_view, name="business"),
    path("business-users/", views.business_users_view, name="businessUsers"),
    path("settings/", views.settings_view, name="settings"),
    path("analytics/", views.analytics_view, name="analytics"),
    path("schedules/", views.schedules_view, name="schedules"),
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

    # categories
    path("categories/", category_views.categories, name="categories"),
    path("edit_category/", category_views.edit_category, name="edit_category"),
    path("delete_category/", category_views.delete_category, name="delete_category"),

#chatbot

    # path('chatbot/ask/', views.chatbot_response, name='chatbot_response'),



]

# ✅ Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
