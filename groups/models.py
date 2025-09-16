from django.db import models
from teachers.models import Teacher   # O‘qituvchini import qildik

class Group(models.Model):
    name = models.CharField(max_length=150)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="groups"
    )
    students_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
