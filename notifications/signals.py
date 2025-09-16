from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task   # sizda Task modeli bor deb hisoblayapman
from .models import Notification

@receiver(post_save, sender=Task)
def task_created(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.teacher,  # kimga yuborish kerak
            title="Yangi vazifa yaratildi",
            message=f"{instance.title} vazifasi qo‘shildi",
            url=f"/tasks/{instance.id}/"
        )
