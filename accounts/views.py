from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, DailyReviewSettingsForm

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


@login_required
def daily_review_settings_view(request):
    """Allow users to update their daily review reminder time at any time"""
    try:
        profile = request.user.profile
    except AttributeError:
        # Create profile if it doesn't exist
        from .models import Profile
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = DailyReviewSettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # Mark that we should show confirmation message
            return render(request, 'accounts/daily_review_settings.html', {
                'form': form,
                'message': 'Daily review reminder time updated successfully!',
                'message_type': 'success'
            })
    else:
        form = DailyReviewSettingsForm(instance=profile)
    
    context = {
        'form': form,
        'current_time': profile.daily_review_time.strftime('%H:%M') if profile.daily_review_time else None
    }
    return render(request, 'accounts/daily_review_settings.html', context)