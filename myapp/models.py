from django.db import models
from django.conf import settings  # use this instead of importing User directly
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Record(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    updated_at= models.DateTimeField(default=timezone.now)  # or auto_now_add=True if preferred
    deleted_at = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Phone number must be entered in the format: '+256789123456'. Up to 15 digits allowed.",
)


class Superadmin(AbstractUser):
    company = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=50, default="SuperAdmin")
    branch = models.CharField(max_length=50, default="MainBranch")
    date = models.DateTimeField(auto_now_add=True)
    # rest of your model ...

    phone_number = models.CharField(max_length=20, blank=True, validators=[phone_regex])

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    deleted_at = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"


class Event(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()  # Fixed: was "models.Dat"
    end = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
