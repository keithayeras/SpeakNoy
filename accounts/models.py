from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    daily_review_time = models.TimeField(null=True, blank=True, help_text="Preferred time to be reminded for daily review")

    def __str__(self):
        return self.user.username