from django.db import models
from teachers.models import Teacher
from groups.models import Group

class Task(models.Model):
    STATUS_CHOICES = (
        ("pending", "Bajarilmagan"),
        ("done", "Bajarilgan"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    assigned_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="tasks")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="tasks")
    
    # Eski boolean o‘rniga status qo‘shamiz
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return self.title
