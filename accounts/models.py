from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, verbose_name="Telefon raqam")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Avatar")
    first_login = models.BooleanField(default=True, verbose_name="Birinchi marta kirish")

    ROLE_CHOICES = (
        ("boss", "Boss"),
        ("teacher", "Teacher"),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="teacher",
        verbose_name="Rol"
    )

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = "boss"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_boss(self):
        return self.role == "boss"

    @property
    def is_teacher(self):
        return self.role == "teacher"


class VerificationCode(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="verification_codes"
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        self.code = str(random.randint(100000, 999999))
        self.save()

    def is_valid(self):
        return (timezone.now() - self.created_at).seconds < 300

    def __str__(self):
        return f"{self.user.username} - {self.code} ({self.created_at})"
