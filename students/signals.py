from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Student
from groups.models import Group

# Student qo‘shilganda yoki yangilanganda
@receiver(post_save, sender=Student)
def update_students_count_on_save(sender, instance, **kwargs):
    group = instance.group
    group.students_count = group.students.count()
    group.save()

# Student o‘chirilganda
@receiver(post_delete, sender=Student)
def update_students_count_on_delete(sender, instance, **kwargs):
    group = instance.group
    group.students_count = group.students.count()
    group.save()
