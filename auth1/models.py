from django.db import models

# https://dev.to/forhadakhan/multi-role-user-authentication-in-django-rest-framework-3nip
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    ROLE_CHOICES = (
        ("employer", "Employer"),
        ("owner", "Owner"),
        ("jobseeker", "jobseeker"),
        ("admin", "admin"),
    )

    role = models.CharField(
        max_length=15, null=True, choices=ROLE_CHOICES, default="jobseeker"
    )
    email = models.EmailField(unique=True)
    isActive = models.BooleanField(default=True)


class Jobseeker(models.Model):
    # other fields related to jobseeker ...
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="jobseeker_account"
    )

    def __str__(self):
        return f"{self.user.email} as a  {self.user.role}"


class Admin(models.Model):
    # other fields related to jobseeker ...
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="admin_account"
    )

    def __str__(self):
        return f"{self.user.email} as a  {self.user.role}"


class Owner(models.Model):
    # other fields related to owner ...
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="owner_account"
    )

    def __str__(self):
        return f"{self.user.email} as a  {self.user.role}"


class Employer(models.Model):
    # other fields related to employer ...
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employer_account"
    )

    def __str__(self):
        return f"{self.user.email} as a  {self.user.role}"
