from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Super Admin'),
        ('COACH', 'Coach'),
        ('CLIENT', 'Client'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coach_profile')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Coach {self.user.username}'

class Client(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='client_profile')
    coach = models.ForeignKey(Coach, null=True, blank=True, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

