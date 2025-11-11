from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
            # return render(request, 'profile.html', {'user': user})
    #     else:
    #         return render(request, 'login.html', {'error': 'Invalid username or password'})
    # else:
    #     return render(request, 'login.html')

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

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

