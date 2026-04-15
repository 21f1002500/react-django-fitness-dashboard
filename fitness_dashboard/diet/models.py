from django.db import models
from accounts.models import Client, Coach

class DietPlan(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='diet_plans')
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True, blank=True, related_name='diet_plans')
    title = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

