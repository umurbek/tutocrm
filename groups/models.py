from django.db import models
from django.db.models import Count, F
from django.utils import timezone
from teachers.models import Teacher 
# Talaba modelini import qilishni unutmang, u Group modeliga bog'liq.
# Agar Student modeli 'students' ilovasida bo'lsa:
# from students.models import Student 

class Group(models.Model):
    # 1. Asosiy ma'lumotlar
    name = models.CharField(max_length=150, verbose_name="Guruh nomi")

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="groups",
        verbose_name="O'qituvchi"
    )

    # 2. Xizmat ma'lumotlari
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Faol / Ochiq"
    )
    
    # Guruhning holatini aniqroq ifodalash uchun qo'shildi (masalan, Dasturlash, Ingliz tili)
    CHOICES = [
        ('IT', 'IT yo\'nalishi'),
        ('Language', 'Tillar'),
        ('Math', 'Aniq fanlar'),
        ('Other', 'Boshqalar'),
    ]
    type = models.CharField(
        max_length=50, 
        choices=CHOICES, 
        default='IT', 
        verbose_name="Yo'nalishi"
    )

    # 3. Vaqt ma'lumotlari
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="So'nggi o'zgarish"
    )
    
    # ----------------------------------------------------------------------
    # Olib tashlandi/O'zgartirildi:
    # ----------------------------------------------------------------------
    # models.PositiveIntegerField tipidagi students_count MAYDONINI O'CHIRDIM. 
    # Sababi: Django Annotation (hisob-kitob) bilan konflikt yuzaga keltirardi. 
    # Talabalar soni endi har doim real-vaqtda hisoblanadi (Annotatsiya orqali).
    # Bu ortiqcha xato va ma'lumotlar nomuvofiqligini oldini oladi.

    # ----------------------------------------------------------------------
    # Qo'shimcha property'lar (real-vaqtda hisoblanadigan funksiyalar)
    # ----------------------------------------------------------------------

    @property
    def get_active_students_count(self):
        """Bu usul guruhdagi faol talabalar sonini qaytaradi."""
        # 'students' related_name Student modelida Group modeliga bog'langan bo'lishi kerak.
        return self.students.filter(is_active=True).count()
    
    @property
    def is_full(self):
        """Guruh to'lgan yoki to'lmaganligini tekshiradi (Agar limit kiritilsa)"""
        # Hozircha doimiy limit yo'q, lekin bu funksiya kelajak uchun foydali.
        return self.get_active_students_count >= 15 # Misol uchun 15 ta limit

    # ----------------------------------------------------------------------

    def __str__(self):
        status = " (Faol)" if self.is_active else " (Yopilgan)"

        teacher_name = "Tayinlanmagan"
        if self.teacher and hasattr(self.teacher, 'user'):
            teacher_name = self.teacher.user.get_full_name()
        
        return f"[{self.get_type_display()}] {self.name} - O'qituvchi: {teacher_name}{status}"

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"
        ordering = ['name'] # Guruhlarni nomi bo'yicha tartiblash
    
# groups/models.py (mavjud Group modelidan keyin qo'shing)

from django.db import models
from django.utils import timezone
from teachers.models import Teacher
# ... (Boshqa importlar) ...


# =========================
# YANGI MODEL: LESSON (DARS JADVALI)
# =========================
# groups/models.py

class Lesson(models.Model):
    LESSON_TYPES = [
        ('regular', 'Oddiy dars'),
        ('test', 'Nazorat'),
        ('extra', 'Qo‘shimcha'),
    ]

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='lessons',  # MUAMMO YO‘Q – BITTA
        verbose_name="Guruh"
    )

    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=90)
    topic = models.CharField(max_length=255, blank=True, null=True)
    lesson_type = models.CharField(
        max_length=10,
        choices=LESSON_TYPES,
        default='regular'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def end_time(self):
        return self.start_time + timezone.timedelta(minutes=self.duration_minutes)

    def __str__(self):
        return f"{self.group.name} - {self.start_time}"
