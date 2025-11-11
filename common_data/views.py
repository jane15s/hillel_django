from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def login_handler(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='teacher').exists():
                return redirect(f'/teacher/{user.id}/')
            elif user.groups.filter(name='student').exists():
                return redirect(f'/student/{user.id}/')
            return render(request, 'login.html',{'error': 'User has no role'})
        return render(request, 'login.html', {'error': 'Invalid credentials'})
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
        role = request.POST["role"]
        try:
            User.objects.get(username=username)
            return render(request, 'login.html', {'error': 'Username already exists'})
        except User.DoesNotExist:
            pass
        new_user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)


        if role.lower() == "teacher":
            new_user.groups.add(Group.objects.get(name='teacher'))
            new_user.is_active = False
        else:
            new_user.groups.add(Group.objects.get(name='student'))

        new_user.save()

        return redirect('/login')
    else:
        return render(request, 'register.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

