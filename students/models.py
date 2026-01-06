from django.db import models
from django.db.models import Sum # Hisob-kitoblar uchun
from groups.models import Group
from accounts.models import CustomUser

# payments ilovasidan Payment modelini import qilish
try:
    from payments.models import Payment
except ImportError:
    # Agar payments app hali to'liq o'rnatilmagan bo'lsa, xato bermasligi uchun
    Payment = None


# =========================
# ASOSIY STUDENT MODEL (CRM uchun)
# =========================
class Student(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='student_profile',
        limit_choices_to={'role': 'student'},
        verbose_name="Tizim foydalanuvchisi",
        null=True,
        blank=True
    )

    # **IZOH:** Bu 'payment' maydonini to'liq o'chirish va uni @property bilan almashtirish mantiqan to'g'ri.
    # Lekin sizning hozirgi kodingizda borligi uchun saqlanib qoldi. Lekin mantiqni Payment modeliga bog'laymiz.
    payment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Oxirgi to'lov summasi",
        default=0.00 # Default qo'shish tavsiya etiladi
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        related_name="students",
        verbose_name="Guruh"
    )

    join_date = models.DateField(
        auto_now_add=True,
        verbose_name="Qo'shilgan sana"
    )
    
    # Yangi maydonlar
    date_of_birth = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Tug‘ilgan sana"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Faol talaba"
    )

    # ----------------------------------------------------
    # DINAMIK XOSSALAR (Payment modeliga asoslangan)
    # ----------------------------------------------------

    @property
    def current_debt(self):
        """O'quvchining to'lanmagan (pending/overdue) to'lovlari summasini hisoblaydi."""
        if Payment:
            # FAQAT kutilayotgan va muddati o'tgan to'lovlarni hisoblaymiz
            debt = self.payments.filter(
                status__in=['pending', 'overdue']
            ).aggregate(Sum('amount'))['amount__sum']
            return debt if debt is not None else 0.00
        return 0.00

    @property
    def is_in_debt(self):
        """Agar joriy qarzdorlik 0 dan katta bo'lsa True qaytaradi."""
        return self.current_debt > 0

    # ----------------------------------------------------

    def __str__(self):
        if self.user:
            return self.user.get_full_name()
        return "Anonim talaba"

    class Meta:
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"


# =========================
# ESKI / O‘QUV UCHUN MODEL (O‘CHIRILMADI)
# =========================
class SimpleStudent(models.Model):
    ism = models.CharField(max_length=100)
    familiya = models.CharField(max_length=100)
    kurs = models.CharField(max_length=50)
    qabul_sana = models.DateField()

    def __str__(self):
        return f"{self.ism} {self.familiya}"