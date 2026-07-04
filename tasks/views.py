from django.http import HttpResponse
from .models import Task

def home(request):
    tasks = Task.objects.all()

    text = ""

    for task in tasks:
        text += f"{task.title}<br>"

    return HttpResponse(text)