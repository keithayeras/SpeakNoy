from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class DailyReviewSettingsForm(forms.ModelForm):
    """Form for updating daily review reminder time"""
    daily_review_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
        }),
        help_text='Set your preferred time for daily review reminders (optional)'
    )

    class Meta:
        model = Profile
        fields = ('daily_review_time',)