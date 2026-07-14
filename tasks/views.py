from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Task
from .forms import TaskForm
from datetime import date
from datetime import datetime
import random
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import openpyxl


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

    today_tasks = Task.objects.filter(
        user=request.user,
        completed=False,
        due_date=date.today()
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
        "today_tasks": today_tasks,

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
    return render(request, "tasks/calendar.html")
from django.http import JsonResponse


@login_required(login_url='login')
def calendar_events(request):

    tasks = Task.objects.filter(user=request.user)

    events = []

    for task in tasks:

        if task.due_date:

            color = "#198754"

            if task.priority == "HIGH":
                color = "#dc3545"

            elif task.priority == "MEDIUM":
                color = "#ffc107"

            events.append({
                "title": task.title,
                "start": task.due_date.strftime("%Y-%m-%d"),
                "url": f"/edit/{task.id}/",
                "color": color,
            })

    return JsonResponse(events, safe=False)
@login_required(login_url='login')
def profile(request):

    total_tasks = Task.objects.filter(
        user=request.user
    ).count()

    completed_tasks = Task.objects.filter(
        user=request.user,
        completed=True
    ).count()

    pending_tasks = Task.objects.filter(
        user=request.user,
        completed=False
    ).count()

    overdue_tasks = Task.objects.filter(
        user=request.user,
        completed=False,
        due_date__lt=date.today()
    ).count()

    progress = 0

    if total_tasks > 0:
        progress = int(
            (completed_tasks / total_tasks) * 100
        )

    context = {

        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "overdue_tasks": overdue_tasks,
        "progress": progress,

    }

    return render(
        request,
        "tasks/profile.html",
        context
    )


@login_required(login_url='login')
def export_pdf(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = 'attachment; filename="tasks.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica", 14)

    p.drawString(200, 800, "Task List")

    y = 760

    tasks = Task.objects.filter(user=request.user)

    for task in tasks:

        status = "Done" if task.completed else "Pending"

        p.drawString(
            50,
            y,
            f"{task.title} | {status}"
        )

        y -= 25

        if y < 50:

            p.showPage()

            y = 800

    p.save()

    return response

@login_required(login_url='login')
def export_excel(request):

    tasks = Task.objects.filter(user=request.user)

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Tasks"

    headers = ["Title", "Description", "Priority", "Status", "Due Date"]
    sheet.append(headers)

    for task in tasks:
        status = "Done" if task.completed else "Pending"
        due_date = task.due_date.strftime("%Y-%m-%d") if task.due_date else ""

        sheet.append([
            task.title,
            task.description,
            task.priority,
            status,
            due_date,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="tasks.xlsx"'

    workbook.save(response)

    return response
