# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


# 🔹 Foydalanuvchi yaratish (Signup) formasi (O'zgarishsiz)
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ("teacher", "Teacher"),
        ("student", "Student"),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
        required=True,
        label="Rol"
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
            "role",
            "password1",
            "password2"
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
            "first_name": forms.TextInput(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
            "last_name": forms.TextInput(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
            "email": forms.EmailInput(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
            "phone": forms.TextInput(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
            "avatar": forms.FileInput(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
            "password1": forms.PasswordInput(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
            "password2": forms.PasswordInput(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
        }


# 🔹 Foydalanuvchi login formasi (O'zgarishsiz)
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "w-full border rounded-lg px-3 py-2"})
        self.fields["password"].widget.attrs.update({"class": "w-full border rounded-lg px-3 py-2"})
        
        
# 🔹 EMAIL ORQALI LOGIN UCHUN FORMA (EmailLoginForm xatosini hal qiladi)
class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500'}),
        required=True
    )