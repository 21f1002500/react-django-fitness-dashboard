from django.db import models
from accounts.models import Coach, Client

class Module(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CoachModuleAccess(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='module_access')
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.coach} - {self.module.name} ({"enabled" if self.is_enabled else "disabled"})'

class AppConfiguration(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

class Analytics(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='analytics')
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    data = models.JSONField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Analytics for {self.client.name} ({self.module.code})'

