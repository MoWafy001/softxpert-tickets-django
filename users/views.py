from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error": "username and password are required"}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful", "username": user.username}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    except Exception as e:
        print(f"Error during login: {e}")
        return JsonResponse({"error": "An error occurred during login"}, status=500)


@login_required
def get_profile(request):
    user = request.user
    profile_data = {
        "username": user.username,
        "name": user.name,
        "role": user.role,
    }
    return JsonResponse(profile_data, status=200)


@csrf_exempt
@login_required
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"}, status=200)

