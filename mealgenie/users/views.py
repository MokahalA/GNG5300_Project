# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile, UserGrocery, GroceryCategory
from django.urls import reverse
from django.http import JsonResponse
import json
from .forms import AddGroceryForm

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
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)
        return redirect('home', username=user.username)
    return render(request, 'register.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request, username):
    user = User.objects.get(username=username)
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    context = {
        'first_name': user.first_name,
        'username': user.username,
        'dietary_preferences': profile.dietary_preferences,
        'allergies': profile.allergies
    }
    return render(request, 'home.html', context)

@login_required
def profile_view(request):
    # Ensure the user profile exists
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "GET":
        user = request.user
        dietary_preferences = json.loads(profile.dietary_preferences) if profile.dietary_preferences else []
        allergies = json.loads(profile.allergies) if profile.allergies else []

        return JsonResponse({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "dietary_preferences": dietary_preferences,
            "allergies": allergies
        })

    elif request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                
                # Update first name and last name
                if 'first_name' in data:
                    request.user.first_name = data['first_name']
                if 'last_name' in data:
                    request.user.last_name = data['last_name']
                request.user.save()

                # Update dietary preferences
                if 'dietary_preferences' in data:
                    profile.dietary_preferences = json.dumps(data['dietary_preferences'])
                    profile.save()

                # Update allergies
                if 'allergies' in data:
                    profile.allergies = json.dumps(data['allergies'])
                    profile.save()

                return JsonResponse({'status': 'success'}, status=200)
                
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    # Convert JSON strings back to lists for rendering in the context
    preferences_list = json.loads(profile.dietary_preferences) if profile.dietary_preferences else []
    allergies_list = json.loads(profile.allergies) if profile.allergies else []

    context = {
        'user': request.user,
        'preferences_json': json.dumps(preferences_list),
        'allergies_json': json.dumps(allergies_list),
    }
    return render(request, 'profile.html', context)

@login_required
def grocery_list_view(request):
    if request.method == 'GET':
        user_groceries = UserGrocery.objects.filter(user=request.user)

        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            grocery_list = [{
                'name': item.grocery_name,
                'category': item.grocery_category.category_name,
                'quantity': item.quantity,
                'unit': item.unit,
                'expiration_date': item.expiration_date.strftime('%Y-%m-%d') if item.expiration_date else None
            } for item in user_groceries]
            return JsonResponse({'groceries': grocery_list})
    return render(request, 'grocery_list.html')

@login_required
def add_grocery_view(request):
    if request.method == 'POST':
        form = AddGroceryForm(request.POST)
        if form.is_valid():
            grocery = form.save(commit=False)
            grocery.user = request.user
            grocery.save()
            return redirect(f"{reverse('home', args=[request.user.username])}#my-groceries")
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form'}, status=400)
    if request.method == 'GET':
        form = AddGroceryForm()
        return render(request, 'add_grocery.html', {'form': form})