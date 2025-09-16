from django.conf import settings
from django.db import models


# 📊 Dashboard statistikasi
class DashboardStat(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dashboard_stats"
    )
    total_students = models.PositiveIntegerField(default=0)
    new_students = models.PositiveIntegerField(default=0)
    graduated_students = models.PositiveIntegerField(default=0)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # 0–100%

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Stats ({self.updated_at.date()})"


# 💸 Oylik xarajatlar
class MonthlyExpense(models.Model):
    CATEGORY_CHOICES = (
        ("rent", "Ijara"),
        ("salary", "Maosh"),
        ("utilities", "Kommunal"),
        ("marketing", "Marketing"),
        ("general", "Umumiy"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses"
    )
    month = models.CharField(max_length=20)  # Masalan: "2025-09"
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="general")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.month} - {self.category}: {self.amount}"


# 📈 Kategoriya bo‘yicha statistikalar
class Statistic(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="statistics"
    )
    category = models.CharField(max_length=100)  # masalan: "Math Students"
    value = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.category}: {self.value}"
