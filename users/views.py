from urllib import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, update_session_auth_hash
from .forms import CustomUserCreationForm, ProfileUpdateForm, CustomPasswordChangeForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after registration
            return redirect("all_posts")  # change to your homepage
    else:
       form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

@login_required(login_url="login")
def profile(request):
    user = request.user
    # Preselect the user’s current group (excluding Admin)
    current_group = user.groups.exclude(name="admin").first()
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("all_posts")  # change to your homepage
    else:
        form = ProfileUpdateForm(instance=user, initial={"group": current_group})
    return render(request, "profile.html", {"form": form})

@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keeps user logged in
            messages.success(request, "Your password has been updated successfully.")
            return redirect("all_posts")
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, "change_password.html", {"form": form})



