# teachers/forms.py

from django import forms
from .models import Teacher
from accounts.models import CustomUser # CustomUser'ni yaratish uchun kerak

# 1. 🍎 Mavjud Teacher profilini tahrirlash formasi (Agar TeacherForm kerak bo'lsa)
class TeacherForm(forms.ModelForm):
    # Bu forma faqat modelda mavjud maydonlarni (CustomUser bog'langanidan so'ng) ishlatadi
    class Meta:
        model = Teacher
        fields = ['user', 'subject', 'is_active'] 
        widgets = {
             'user': forms.Select(attrs={'class': 'w-full border rounded-lg px-3 py-2'}), 
             'subject': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
             'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5'}),
        }
        labels = {
            "user": "Tizim foydalanuvchisi",
            "subject": "O'qitadigan fani",
            "is_active": "Faol o'qituvchi"
        }


# 2. ➕ Yangi Teacher va CustomUser'ni bir vaqtda yaratish formasi (Sizning asosiy maqsadingiz)
class TeacherCreateForm(forms.ModelForm):
    # CustomUser'dan olinadigan maydonlar
    first_name = forms.CharField(max_length=150, required=True, label="Ism", 
                                 widget=forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}))
    last_name = forms.CharField(max_length=150, required=True, label="Familiya",
                                widget=forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}))
    email = forms.EmailField(required=True, label="Email",
                             widget=forms.EmailInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}))
    phone = forms.CharField(max_length=20, required=True, label="Telefon",
                            widget=forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}), label="Parol")

    class Meta:
        model = Teacher
        # Teacher modelining qolgan maydonlari
        fields = ['subject'] 
        widgets = {
             'subject': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
        }
        
    def save(self, commit=True):
        # 1. CustomUser'ni yaratish
        user = CustomUser.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone=self.cleaned_data['phone'],
            role='teacher', # Rolni avtomatik 'teacher' deb belgilash
        )
        
        # 2. Teacher profilini CustomUserga bog'lash
        teacher = super().save(commit=False)
        teacher.user = user
        if commit:
            teacher.save()
        return teacher