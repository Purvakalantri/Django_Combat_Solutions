from django.db import models
from django.contrib.auth.models import User
# from .signals import update_status

class Complaint(models.Model):

    class Meta:
        db_table = 'complaints'

    class Priority(models.TextChoices):
        LOW= 'Low', "low"
        MEDIUM='Medium',"medium"
        HIGH='High', 'high'

    priority = models.CharField(
        choices=Priority.choices,
        null=True,
        default=None
    )

    class Status(models.TextChoices):
        PENDING= 'Pending', "pending"
        IN_PROGRESS='In Progress',"in progress"
        RESOLVED='Resolved', 'resolved'

    status = models.CharField(
        choices=Status.choices,
        default=Status.PENDING
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='complaints'
    )

    title = models.CharField(max_length=100)
    description=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title


