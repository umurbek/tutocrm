from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "phone", "avatar", "password1", "password2"]
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


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "w-full border rounded-lg px-3 py-2"})
        self.fields["password"].widget.attrs.update({"class": "w-full border rounded-lg px-3 py-2"})
