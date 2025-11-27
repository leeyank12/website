from django.shortcuts import render, redirect
from .models import User, DiaryEntry
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password

def registerView(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")
        
        User.objects.create(
            fullname=fullname,
            email=email,
            password=make_password(password)
        )

        messages.success(request, "Registration successful!")
        return redirect("login")

    return render(request, "register.html")


def loginView(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(email=email).first()

        if user and check_password(password,user.password):
            request.session['user_id'] = str(user.id)
            request.session['user_name'] = user.fullname
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    return render(request, "login.html")


def homeView(request):
    if 'user_id' not in request.session:
        return redirect("login")

    name = request.session.get('user_name')
    entries = DiaryEntry.objects.filter(user_id=request.session['user_id'])

    return render(request, "home.html", {"name": name, "entries": entries})
