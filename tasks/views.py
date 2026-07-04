from django.http import HttpResponse

def home(request):
    return HttpResponse("🔥 سایت درست بالا اومد")