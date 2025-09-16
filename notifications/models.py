from django.db import models
from teachers.models import Teacher

class Notification(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    url = models.CharField(max_length=500, blank=True, null=True)  # masalan: /tasks/5/
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} -> {self.teacher.name}"
