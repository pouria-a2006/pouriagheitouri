from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from datetime import date


@login_required(login_url='login')
def home(request):

    filter_type = request.GET.get("filter")
    search = request.GET.get("search")

    tasks = Task.objects.filter(user=request.user)

    if search:
        tasks = tasks.filter(title__icontains=search)

    if filter_type == "completed":
        tasks = tasks.filter(completed=True)

    elif filter_type == "pending":
        tasks = tasks.filter(completed=False)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()
    overdue_tasks = tasks.filter(
    completed=False,
    due_date__lt=date.today()
    ).count()

    progress = 0

    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)

    

    context = {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "overdue_tasks": overdue_tasks,
        "progress": progress,
    }

    return render(request, "tasks/home.html", context)


@login_required(login_url='login')
def add_task(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)
            task.user = request.user
            task.save()

            return redirect('home')

        print(form.errors)

    else:

        form = TaskForm()

    return render(request, "tasks/add_task.html", {"form": form})


@login_required(login_url='login')
def delete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    task.delete()

    return redirect('home')


@login_required(login_url='login')
def toggle_complete(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    task.completed = not task.completed
    task.save()

    return redirect('home')


@login_required(login_url='login')
def edit_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == "POST":

        form = TaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():
            form.save()
            return redirect('home')

    else:

        form = TaskForm(instance=task)

    return render(
        request,
        "tasks/edit_task.html",
        {"form": form}
    )