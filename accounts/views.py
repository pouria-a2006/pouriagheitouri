from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required




# 🔐 Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "accounts/login.html", {"error": "اطلاعات اشتباه است"})

    return render(request, "accounts/login.html")


# 📝 Register
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {"error": "این نام کاربری وجود دارد"})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')

    return render(request, "accounts/register.html")


# 🚪 Logout
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url="login")
def edit_profile(request):

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            return redirect("profile")

    else:

        form = ProfileForm(
            instance=request.user
        )

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form
        }
    )