from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-@_rg(@jfq$kly7i2s&ct&=zytikp&l@e!o*r%xhzmm#_a79o@x"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ------------------------
# Custom User
# ------------------------
AUTH_USER_MODEL = "accounts.CustomUser"


# settings.py

JAZZMIN_SETTINGS = {
    # Sayt sarlavhasi (brauzer tabida)
    "site_title": "TutoCRM Boshqaruvi",

    # Admin panelning asosiy sarlavhasi
    "site_header": "TutoCRM",

    # Chap menyudagi yopish/ochish tugmasini o'chirish
    "navigation_expanded": False,
    "custom_css": "css/jazzmin_glass.css",
    "topmenu_links": [

        # Asosiy Dashboard uchun Home tugmasi
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # O'zingizning Students (Talabalar) modelingizga havola
        {"name": "Talabalar", "url": "/admin/school/student/", "icon": "fas fa-users"},
        
        # O'zingizning Teachers (O'qituvchilar) modelingizga havola
        {"name": "O'qituvchilar", "url": "/admin/school/teacher/", "icon": "fas fa-chalkboard-teacher"},
        
        # Admin ilovalarini ochadigan umumiy menyu (zarur bo'lsa)
        {"model": "auth.User"},
        ],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "united",  # 'united', 'cosmo', 'superhero', 'darkly' kabi ko'plab mavzular mavjud
    "sidebar": "sidebar-dark-primary",
    "navbar_classes": "navbar-light navbar-warning",
    # Qo'shimcha sozlamalar uchun Jazzmin hujjatlariga qarang
}
# ------------------------
# Application definition
# ------------------------
INSTALLED_APPS = [
    'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.humanize',
    # allauth uchun
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    # Local apps
    "accounts",
    "home",
    "dashboard",
    "groups",
    "students",
    "teachers",
    "tasks",
    "settingsapp",
    "notifications",
    "chat",
    "payments",
    "schedule",
    "lessons",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tutocrm.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",  # allauth ishlashi uchun kerak
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.user_avatar",
                "notifications.context_processors.unread_notifications",
                'notifications.context_processors.unread_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = "tutocrm.wsgi.application"

# ------------------------
# Database
# ------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ------------------------
# Password validation
# ------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------
# Authentication
# ------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",  # Google login uchun
]

LOGIN_URL = "email_login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "email_login"

# allauth sozlamalari
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"

# ------------------------
# Email sozlamalari
# ------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "umurbekfaridov8@gmail.com"
EMAIL_HOST_PASSWORD = "iwycodnvbojkxiyh"  # Gmail App Password ishlatish shart!
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# settings.py
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_SIGNUP_REDIRECT_URL = "dashboard"  # Google orqali kira qolsa, qayerga redirect bo‘lsin
# settings.py
SOCIALACCOUNT_AUTO_SIGNUP = True     # Oraliq "Sign Up" form chiqmaydi
ACCOUNT_EMAIL_VERIFICATION = "none"  # Email tasdiqlash ham chiqmaydi

SOCIALACCOUNT_ADAPTER = "accounts.adapter.NoSignupAdapter"

# ------------------------
# Internationalization
# ------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

# ------------------------
# Static & Media files
# ------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
# settings.py ning pastki qismida

# Statik fayllarning URL manzili (brauzer uchun)
STATIC_URL = 'static/'

# **********************************************
# Quyidagi qatorni qo'shing (Xatolikni tuzatish uchun)
# Bu collectstatic buyrug'i statik fayllarni yig'adigan manzil
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# **********************************************

# Loyihaning o'zidagi statik fayllar uchun qo'shimcha papka (ixtiyoriy)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------
# Default primary key
# ------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
