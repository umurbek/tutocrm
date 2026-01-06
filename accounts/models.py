# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone 
import random


class CustomUser(AbstractUser):
    """
    Tizim foydalanuvchilari uchun maxsus model. 
    Rolga asoslangan tizim va avatarni qo'llab-quvvatlaydi.
    """
    ROLE_CHOICES = (
        ("boss", "Boss"),
        ("teacher", "Teacher"),
        ("student", "Student"), 
    )
    
    # Qo'shimcha maydonlar
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Telefon raqam")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Avatar")
    first_login = models.BooleanField(default=True, verbose_name="Birinchi marta kirish")
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student",
        verbose_name="Rol"
    )

    def save(self, *args, **kwargs):
        # Superuser har doim boss rolida bo‘ladi
        if self.is_superuser:
            self.role = "boss"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    # Rol tekshiruvlari (Properties)
    @property
    def is_boss(self):
        """Foydalanuvchi Boss (Admin) rolidami?"""
        return self.role == "boss"

    @property
    def is_teacher(self):
        """Foydalanuvchi O'qituvchi rolidami?"""
        return self.role == "teacher"

    @property
    def is_student(self):
        """Foydalanuvchi O'quvchi rolidami?"""
        return self.role == "student"


class VerificationCode(models.Model):
    """
    Email orqali login uchun 6 xonali tasdiqlash kodini saqlash modeli.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="verification_codes"
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        """Tasodifiy 6 xonali kod yaratadi va saqlaydi."""
        self.code = str(random.randint(100000, 999999))
        # Yangi yaratilgan kodni DBga saqlash
        self.save()

    def is_valid(self):
        """Kodning amal qilish muddatini (5 daqiqa) tekshiradi."""
        return (timezone.now() - self.created_at).total_seconds() < 300

    def __str__(self):
        return f"{self.user.username} - {self.code}"