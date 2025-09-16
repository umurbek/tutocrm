from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

@login_required
def index(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "chat/room.html", {"users": users})

@login_required
def room(request, user_id):
    users = User.objects.exclude(id=request.user.id)
    selected_user = get_object_or_404(User, id=user_id)
    return render(request, "chat/room.html", {
        "users": users,
        "selected_user": selected_user
    })

@login_required
def get_messages(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")

    data = []
    for m in messages:
        data.append({
            "text": m.text,
            "from_me": m.sender == request.user,
            "timestamp": m.timestamp.strftime("%d.%m.%Y %H:%M"),
        })
    return JsonResponse({"messages": data})

@login_required
def send_message(request, user_id):
    import json
    data = json.loads(request.body)
    text = data.get("text")

    receiver = get_object_or_404(User, id=user_id)
    Message.objects.create(sender=request.user, receiver=receiver, text=text)
    return JsonResponse({"status": "ok"})
