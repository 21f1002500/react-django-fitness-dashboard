from django.db import models
from accounts.models import Coach

class Subscription(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    )

    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='subscriptions')
    plan_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.plan_name} for {self.coach.user.username}'

