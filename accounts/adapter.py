from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class NoSignupAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        # Har doim avtomatik ro‘yxatdan o‘tkazish
        return True

    def save_user(self, request, sociallogin, form=None):
        # Standart user yaratish
        user = super().save_user(request, sociallogin, form)
        return user
