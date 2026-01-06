from django.db import models
from django.contrib.auth import get_user_model
# Guruh va Talaba modellarini import qilish
from groups.models import Group 
from students.models import Student 

User = get_user_model()

# =============================================================
# 🏢 Task Modeli (Vazifaning umumiy tavsifi)
# =============================================================
class Task(models.Model):
    STATUS_CHOICES = (
        ("pending", "Bajarilmagan"),
        ("done", "Bajarilgan"),
    )
    
    TASK_TYPE_CHOICES = (
        ("Group", "Guruhga"),
        # Shaxsiy o'quvchiga vazifa berish uchun
        ("Student", "Shaxsiy o'quvchiga"), 
    )

    title = models.CharField(max_length=200, verbose_name="Vazifa nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    due_date = models.DateField(verbose_name="Topshirish muddati")
    
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="tasks_created", 
        verbose_name="Beruvchi"
    )
    
    task_type = models.CharField(
        max_length=10, 
        choices=TASK_TYPE_CHOICES, 
        default="Group", 
        verbose_name="Vazifa turi"
    )
    
    target_group = models.ForeignKey(
        Group, 
        on_delete=models.SET_NULL, # Vazifa turib qolishi uchun CASCADE emas, SET_NULL yaxshi
        null=True, 
        blank=True, 
        related_name="tasks", 
        verbose_name="Guruh"
    )
    
    target_student = models.ForeignKey(
        Student, 
        on_delete=models.SET_NULL, # Vazifa turib qolishi uchun CASCADE emas, SET_NULL yaxshi
        null=True, 
        blank=True, 
        related_name="tasks", 
        verbose_name="O'quvchi (Shaxsiy)"
    )
    
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default="pending", 
        verbose_name="Umumiy Holati" # Task Assignment dan farqlash uchun "Umumiy" qo'shildi
    )

    def __str__(self):
        target = self.target_group.name if self.target_group else (
            self.target_student.user.get_full_name() if self.target_student else "Belgilanmagan"
        )
        return f"{self.title} ({self.task_type} | {target})"

    class Meta:
        verbose_name = "Vazifa"
        verbose_name_plural = "Vazifalar"
        ordering = ['due_date', 'title'] # Tartiblash qo'shildi


# =============================================================
# 🧑‍🎓 TaskAssignment Modeli (Har bir Talabaning shaxsiy holati)
# =============================================================
class TaskAssignment(models.Model):
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='assignments', 
        verbose_name="Vazifa"
    )
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='task_assignments', 
        verbose_name="O'quvchi"
    )
    
    is_completed = models.BooleanField(default=False, verbose_name="Bajarilgan")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Bajarilgan sana")
    
    # Qo'shimcha: O'qituvchi tomonidan tekshirish/baholash uchun
    feedback = models.TextField(blank=True, verbose_name="Izoh/Baholash")
    
    class Meta:
        # Bir o'quvchiga bir vazifa faqat bir marta tayinlanishi mumkin
        unique_together = ('task', 'student') 
        verbose_name = "Vazifa tayinlash"
        verbose_name_plural = "Vazifalar tayinlash"
        
    def __str__(self):
        status = "✅ Bajarilgan" if self.is_completed else "❌ Kutilmoqda"
        return f"'{self.task.title}' -> {self.student}: {status}"