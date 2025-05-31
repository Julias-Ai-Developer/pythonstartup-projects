# myapp/models.py
from django.db import models
from django.contrib.auth.models import User


class Record(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    status = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.category_name

    class Meta:  # ✅ Correct — nested inside the model
        verbose_name_plural = "Categories"
