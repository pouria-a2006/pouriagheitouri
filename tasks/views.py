from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

def home(request):
    filter_type = request.GET.get("filter")
    search = request.GET.get("search")

    tasks = Task.objects.all()

    if search:
        tasks = tasks.filter(title__icontains=search)

    if filter_type == "completed":
        tasks = tasks.filter(completed=True)

    elif filter_type == "pending":
        tasks = tasks.filter(completed=False)

    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    pending_tasks = Task.objects.filter(completed=False).count()

    context = {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
    }

    return render(request, "tasks/home.html", context)
    return render(request, "tasks/home.html", context)
    return render(request, "tasks/home.html", {"tasks": tasks})
def add_task(request):
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, "tasks/add_task.html", {"form": form})
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('home')
def toggle_complete(request, task_id):
    task = Task.objects.get(id=task_id)

    task.completed = not task.completed
    task.save()

    return redirect('home')
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/edit_task.html", {"form": form})