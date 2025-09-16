from .utils import get_gravatar_url

def user_avatar(request):
    if request.user.is_authenticated:
        return {"avatar_url": get_gravatar_url(request.user.email, 80)}
    return {"avatar_url": "https://i.pravatar.cc/80"}
