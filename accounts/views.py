from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms

from .models import CustomUser, VerificationCode
from .forms import CustomUserCreationForm


# 🔹 Ro‘yxatdan o‘tish
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # backendni aniq ko‘rsatamiz
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("dashboard:dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

# 🔹 Profil
@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"user": request.user})


# 🔹 Email orqali login
def email_login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return render(request, "accounts/email_login.html", {"error": "Bunday email topilmadi"})

        vc = VerificationCode.objects.create(user=user)
        vc.generate_code()
        send_mail(
            "TutorCRM - Tasdiqlash kodi",
            f"Sizning tasdiqlash kodingiz: {vc.code}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        request.session["pending_user"] = user.id
        return redirect("accounts:verify_code")

    return render(request, "accounts/email_login.html")


# 🔹 Kodni tekshirish
def verify_code_view(request):
    if request.method == "POST":
        code = request.POST.get("code")
        user_id = request.session.get("pending_user")

        if not user_id:
            return redirect("accounts:email_login")

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return redirect("accounts:email_login")

        vc = VerificationCode.objects.filter(user=user).last()
        if vc and vc.is_valid() and vc.code == code:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            del request.session["pending_user"]

            if user.first_login:
                user.first_login = False
                user.save()
                return redirect("accounts:welcome")

            return redirect("dashboard:dashboard")

        return render(request, "accounts/verify_code.html", {"error": "Kod noto‘g‘ri yoki muddati o‘tgan"})

    return render(request, "accounts/verify_code.html")


# 🔹 Dashboard
@login_required
def dashboard_view(request):
    user = request.user
    if user.is_teacher:
        return render(request, "dashboard/teacher_dashboard.html", {"user": user})
    if user.is_boss:
        return render(request, "dashboard/boss_dashboard.html", {"user": user})
    return render(request, "dashboard/index.html", {"user": user})


# 🔹 Profilni tahrirlash
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "border rounded w-full p-2"}),
            "last_name": forms.TextInput(attrs={"class": "border rounded w-full p-2"}),
            "email": forms.EmailInput(attrs={"class": "border rounded w-full p-2"}),
        }


@login_required
def profile_edit_view(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi ✅")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=user)
    return render(request, "accounts/profile_edit.html", {"form": form})


# 🔹 Welcome sahifasi
@login_required
def welcome_view(request):
    return render(request, "accounts/welcome.html")
