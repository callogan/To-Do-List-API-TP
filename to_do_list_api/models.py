from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = [("P", "Pending"), ("IP", "In-progress"), ("C", "Completed")]

    title = models.TextField()
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="P")

    class Meta:
        ordering = ["status"]
