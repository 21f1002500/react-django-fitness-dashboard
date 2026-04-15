from django.db import models
from accounts.models import Client, Coach

class Tracker(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tracker_records')
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracker_records')
    data = models.JSONField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.client.name} - {self.date}'
