from django.db import models
from django.utils import timezone

# Boshqa ilovalardan kerakli modellarni import qilish
# student modeli studentlar ilovasida bo'lishi kerak
from students.models import Student 
# Agar Paymentni yaratgan CustomUser (Boss/Admin) ni saqlash kerak bo'lsa, uni import qiling
# from accounts.models import CustomUser 


class Payment(models.Model):
    """O'quvchilarning to'lovlari va hisob-kitoblarini saqlash modeli."""

    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda (Qarzdorlik)'),
        ('completed', 'To\'langan'),
        ('overdue', 'Muddati o\'tgan'),
        ('canceled', 'Bekor qilingan'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="O\'quvchi"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Miqdori (so\'mda)"
    )

    # To'lov olinishi kerak bo'lgan muddat
    due_date = models.DateField(
        verbose_name="To\'lov muddati"
    )

    # Haqiqatda to'lov qilingan sana
    payment_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="To\'lov qilingan sana"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Holati"
    )
    
    # Izohlar yoki kim tomonidan qo'shilgani
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Izoh"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "To\'lov"
        verbose_name_plural = "To\'lovlar"
        ordering = ['due_date', 'status']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.amount} ({self.status})"
    
    def check_overdue(self):
        """Agar to'lov muddati o'tgan bo'lsa, holatini yangilaydi."""
        if self.status == 'pending' and self.due_date < timezone.now().date():
            self.status = 'overdue'
            self.save()
            return True
        return False

# models.py ga Payment modelini yozib bo'lgach, uni migratsiya qilishingiz kerak!