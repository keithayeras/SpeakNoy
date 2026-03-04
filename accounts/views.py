from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/SpeakNoy")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('accounts:login')
    return redirect('SpeakNoy:cardlist')