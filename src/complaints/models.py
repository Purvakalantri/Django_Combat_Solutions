from django.db import models

class Complaint(models.Model):

    class Meta:
        db_table = 'complaints'

    class Priority(models.TextChoices):
        LOW= 'Low', "low"
        MEDIUM='Medium',"medium"
        HIGH='High', 'high'

    priority = models.CharField(
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    class Status(models.TextChoices):
        PENDING= 'Pending', "pending"
        IN_PROGRESS='In Progress',"in progress"
        RESOLVED='Resolved', 'resolved'

    status = models.CharField(
        choices=Status.choices,
        default=Status.PENDING
    )


    title = models.CharField(max_length=100)
    description=models.TextField()




