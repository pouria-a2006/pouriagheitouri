from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Task(models.Model):

    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    completed = models.BooleanField(default=False)

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    due_date = models.DateField(
        null=True,
        blank=True
    )

    def is_overdue(self):
        return (
            self.due_date is not None
            and self.due_date < date.today()
            and not self.completed
        )

    def __str__(self):
        return self.title