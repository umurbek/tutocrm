from django.db import models
from groups.models import Group

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="students")
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
