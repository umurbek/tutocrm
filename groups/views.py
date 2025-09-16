from django.shortcuts import render, redirect, get_object_or_404
from .models import Group
from .forms import GroupForm


# 📋 Guruhlar ro‘yxati
def group_list(request):
    groups = Group.objects.all()
    return render(request, "groups/group_list.html", {"groups": groups})


# ➕ Yangi guruh qo‘shish
def group_create(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("groups:group_list")
    else:
        form = GroupForm()
    return render(request, "groups/group_form.html", {"form": form})


# ✏️ Guruhni tahrirlash
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect("groups:group_list")
    else:
        form = GroupForm(instance=group)
    return render(request, "groups/group_form.html", {"form": form})


# ❌ Guruhni o‘chirish
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":   # xavfsizroq usul
        group.delete()
        return redirect("groups:group_list")
    return render(request, "groups/group_confirm_delete.html", {"group": group})


# 🔍 Guruh detail
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    return render(request, "groups/group_detail.html", {"group": group})
