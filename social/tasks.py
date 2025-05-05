from celery import shared_task
from django.contrib.auth.models import User
from .models import Notification

@shared_task
def send_notification(sender_id, recipient_id, message):
    sender = User.objects.get(id=sender_id)
    recipient = User.objects.get(id=recipient_id)
    Notification.objects.create(
        sender=sender,
        recipient=recipient,
        message=message
    )