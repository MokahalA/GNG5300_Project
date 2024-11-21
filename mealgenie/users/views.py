# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile, UserGrocery, Grocery, GroceryCategory
from django.http import JsonResponse
import json

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
def my_groceries_view(request):
    if request.method == 'GET':
        # Get user's groceries
        print(f"Current user: {request.user.username}")
        user_groceries = UserGrocery.objects.filter(user=request.user).select_related('grocery')
        
        # Format data for JSON response
        grocery_list = [{
            'name': item.grocery.name,
            'quantity': item.quantity,
            'unit': item.grocery.unit,
            'expiration_date': item.expiration_date.strftime('%Y-%m-%d') if item.expiration_date else None
        } for item in user_groceries]
        
        return JsonResponse({'groceries': grocery_list})
    
    return render(request, 'grocery_list.html')