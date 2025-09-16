# accounts/utils.py
import hashlib

def get_gravatar_url(email, size=100):
    """
    Berilgan email bo‘yicha gravatar URL qaytaradi.
    Agar foydalanuvchi avatar yuklamagan bo‘lsa, gravatardan foydalaniladi.
    """
    email = email.lower().encode("utf-8")
    hash_email = hashlib.md5(email.strip()).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_email}?s={size}&d=identicon"
