from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.http import JsonResponse
from .auth_form import RegisterForm, LoginForm
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return JsonResponse({"message": "User Registered successfully", "user_id": user.id}, status=201)
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())

            # Generate JWT tokens
            refresh = RefreshToken.for_user(form.get_user())
            access_token = str(refresh.access_token)

            return JsonResponse({
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": str(refresh)
            }, status=200)
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

