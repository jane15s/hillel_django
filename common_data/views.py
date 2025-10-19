from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def login_handler(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'profile.html', {'user': user})
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def logout_handler(request):
    logout(request)
    return redirect('/login')

def register_handler(request):
    if request.method == 'POST':
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            User.objects.get(username=username)
            return render(request, 'login.html', {'error': 'Username already exists'})
        except User.DoesNotExist:
            pass
        new_user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        new_user.save()
        return redirect('/login')
    else:
        return render(request, 'register.html')

