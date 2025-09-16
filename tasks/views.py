from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from notifications.models import Notification


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()

            # 🔔 Notification yaratish
            Notification.objects.create(
                teacher=task.assigned_teacher,
                title=f"Yangi vazifa: {task.title}",
                message=f"{task.group.name} guruhi uchun vazifa. Muddat: {task.due_date}",
                url=f"/tasks/{task.id}/",
            )

            return redirect('tasks:task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('tasks:task_list')


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


def task_complete(request, pk):
    """ ✅ Vazifani bajarilgan deb belgilash """
    task = get_object_or_404(Task, pk=pk)
    task.status = "done"
    task.save()
    return redirect('tasks:task_detail', pk=pk)
from django.views.decorators.http import require_POST

@require_POST
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = "done"
    task.save()
    return redirect("tasks:task_detail", pk=pk)
