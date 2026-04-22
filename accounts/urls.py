from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup_view, logout_view, daily_review_settings_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('daily-review-settings/', daily_review_settings_view, name='daily_review_settings'),
]

app_name = 'accounts'