from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email      = request.POST.get('email')
        password1  = request.POST.get('password1')
        password2  = request.POST.get('password2')
        country    = request.POST.get('country')
        user_type  = request.POST.get('user_type', 'tourist')

        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('register')

        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters!')
            return redirect('register')

        # Create user
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            country=country,
            user_type=user_type,
        )

        # Log them in immediately
        login(request, user)
        messages.success(request, f'Welcome to SafariGrants, {first_name}!')
        return redirect('dashboard')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate
        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password!')
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')


def dashboard_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to access your dashboard!')
        return redirect('login')
    return render(request, 'dashboard.html')