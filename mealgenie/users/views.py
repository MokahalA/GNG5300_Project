# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home', username=user.username)
        else:
            context = {'error': 'Invalid username or password'}
            return render(request, 'login.html', context)
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        login(request, user)
        return redirect('home', username=user.username)
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request, username):
    user = User.objects.get(username=username)
    context = {'first_name': user.first_name, 'username': user.username}
    return render(request, 'home.html', context)