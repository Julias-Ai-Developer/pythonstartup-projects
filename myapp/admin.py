from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Record, Category, Superadmin


class SuperadminAdmin(UserAdmin):
    model = Superadmin
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "company",
        "branch",
        "role",
        "phone_number",
        "is_staff",
    )
    search_fields = ("username", "email", "company", "branch")
    list_filter = ("is_staff", "is_superuser", "company", "branch")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Info",
            {
                "fields": ("company", "branch", "role", "phone_number"),
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Info",
            {
                "fields": ("company", "branch", "role", "phone_number"),
            },
        ),
    )

    

admin.site.register(Superadmin, SuperadminAdmin)
admin.site.register(Record)
admin.site.register(Category)
