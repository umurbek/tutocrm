# teachers/models.py

from django.db import models
# 💡 CustomUser modelini import qilishni unutmang
from accounts.models import CustomUser 

class Teacher(models.Model):
    # CustomUser bilan bog'lash (Bu asosiy o'zgarish)
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='teacher_profile',
        limit_choices_to={'role': 'teacher'}, # Faqat 'teacher' roliga ega userlar tanlansin
        verbose_name="Tizim foydalanuvchisi"
    )

    # Oldingi maydonlar (name, email, phone endi user modelidan olinadi)
    # subject maydoni alohida qoladi
    
    subject = models.CharField(max_length=100, verbose_name="O'qitadigan fani")
    join_date = models.DateField(auto_now_add=True, verbose_name="Ishga kirgan sana")
    
    is_active = models.BooleanField(default=True, verbose_name="Faol o'qituvchi")

    def __str__(self):
        # Name endi CustomUser modelidan olinadi
        return f"{self.user.get_full_name()} ({self.subject})"
        
    class Meta:
        verbose_name = "O'qituvchi"
        verbose_name_plural = "O'qituvchilar"

        