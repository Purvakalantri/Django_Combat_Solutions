from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import Complaint
import threading
import time

def delayed_status_update(complaint_id):
    time.sleep(30)
    from src.complaints.models import Complaint
    complaint = Complaint.objects.get(id=complaint_id)
    complaint.status = 'RESOLVED'
    complaint.save(update_fields=["status"])

@receiver(post_save, sender=Complaint)
def update_status(sender, instance, created, **kwargs):
    if not created:
        return

    instance.status = 'IN_PROGRESS'
    instance.save(update_fields=["status"])

    threading.Thread(
        target=delayed_status_update,
        args=(instance.id,),
        daemon=True
    ).start()


