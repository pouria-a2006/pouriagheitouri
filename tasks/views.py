from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Task
from .forms import TaskForm
from datetime import date
from datetime import datetime
import random


@login_required(login_url='login')
def home(request):

    filter_type = request.GET.get("filter")
    search = request.GET.get("search")

    # همه تسک‌های کاربر
    tasks = Task.objects.filter(user=request.user)

    # جستجو
    if search:
        tasks = tasks.filter(title__icontains=search)

    # فیلتر
    if filter_type == "completed":
        tasks = tasks.filter(completed=True)

    elif filter_type == "pending":
        tasks = tasks.filter(completed=False)

    # آمار (قبل از صفحه‌بندی)
    total_tasks = tasks.count()

    completed_tasks = tasks.filter(
        completed=True
    ).count()

    pending_tasks = tasks.filter(
        completed=False
    ).count()

    overdue_tasks = tasks.filter(
        completed=False,
        due_date__lt=date.today()
    ).count()

    # درصد پیشرفت
    progress = 0

    if total_tasks > 0:
        progress = int(
            (completed_tasks / total_tasks) * 100)
        

    # Pagination
    paginator = Paginator(tasks, 5)

    page_number = request.GET.get("page")

    tasks = paginator.get_page(page_number)

    hour = datetime.now().hour

    if hour < 12:
        greeting = "☀️ Good Morning"
    elif hour < 18:
        greeting = "🌤️ Good Afternoon"
    else:
        greeting = "🌙 Good Evening"
  

    quotes = [
        "💡 Small progress is still progress.",
        "🚀 Stay focused and never give up.",
        "🔥 Success comes from consistency.",
        "🎯 Every task completed is a step forward.",
        "📚 Keep learning every day."
    ]

    quote = random.choice(quotes) 

    context = {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "overdue_tasks": overdue_tasks,
        "progress": progress,
        "user": request.user,
        "member_since": request.user.date_joined,
        "greeting": greeting,
        "quote": quote,

    }

    return render(
        request,
        "tasks/home.html",
        context
    )


@login_required(login_url='login')
def add_task(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)
            task.user = request.user
            task.save()

            task.save()

            messages.success(request, "Task added successfully ✅")

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

    messages.error(request, "Task deleted successfully 🗑️")

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

    if task.completed:
        messages.success(request, "Task completed 🎉")
    else:
        messages.warning(request, "Task marked as pending ⏳")

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

            messages.info(request, "Task updated successfully ✏️")

            return redirect('home')

    else:

        form = TaskForm(instance=task)

    return render(
        request,
        "tasks/edit_task.html",
        {"form": form}
    )

@login_required(login_url='login')
def calendar_view(request):

        return render(
            request,
            "tasks/calendar.html"
    )