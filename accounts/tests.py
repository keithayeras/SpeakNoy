from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, time
from .models import Profile
from .forms import DailyReviewSettingsForm


class ProfileModelTest(TestCase):
    """Test the Profile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
    
    def test_profile_creation(self):
        """Test that a profile is created with a user"""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)
    
    def test_daily_review_time_field(self):
        """Test that daily_review_time field stores time correctly"""
        profile = self.user.profile
        test_time = time(14, 30)
        profile.daily_review_time = test_time
        profile.save()
        
        profile.refresh_from_db()
        self.assertEqual(profile.daily_review_time, test_time)
    
    def test_daily_review_time_null_by_default(self):
        """Test that daily_review_time is null by default"""
        profile = self.user.profile
        self.assertIsNone(profile.daily_review_time)


class DailyReviewSettingsFormTest(TestCase):
    """Test the DailyReviewSettingsForm"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = self.user.profile
    
    def test_form_with_valid_time(self):
        """Test form with valid time"""
        form_data = {'daily_review_time': '14:30'}
        form = DailyReviewSettingsForm(form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
    
    def test_form_with_empty_time(self):
        """Test form with empty time (optional field)"""
        form_data = {'daily_review_time': ''}
        form = DailyReviewSettingsForm(form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
    
    def test_form_saves_time_correctly(self):
        """Test that form saves time to profile"""
        form_data = {'daily_review_time': '09:00'}
        form = DailyReviewSettingsForm(form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
        form.save()
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.daily_review_time, time(9, 0))


class DailyReviewSettingsViewTest(TestCase):
    """Test the daily review settings view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = self.user.profile
        self.url = reverse('accounts:daily_review_settings')
    
    def test_view_requires_login(self):
        """Test that view requires authentication"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_view_accessible_to_authenticated_user(self):
        """Test that authenticated users can access the view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_displays_form(self):
        """Test that view displays the form"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertIn('form', response.context)
    
    def test_post_updates_settings(self):
        """Test that POST request updates daily review time"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, {'daily_review_time': '15:45'})
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.daily_review_time, time(15, 45))
    
    def test_post_shows_success_message(self):
        """Test that successful POST shows success message"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, {'daily_review_time': '10:30'})
        
        self.assertIn('message', response.context)
        self.assertIn('success', response.context.get('message_type', ''))
    
    def test_can_clear_daily_review_time(self):
        """Test that users can clear their daily review time"""
        self.profile.daily_review_time = time(14, 0)
        self.profile.save()
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, {'daily_review_time': ''})
        
        self.profile.refresh_from_db()
        self.assertIsNone(self.profile.daily_review_time)
    
    def test_multiple_time_changes(self):
        """Test that user can change time multiple times"""
        self.client.login(username='testuser', password='testpass123')
        
        # First change
        self.client.post(self.url, {'daily_review_time': '08:00'})
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.daily_review_time, time(8, 0))
        
        # Second change
        self.client.post(self.url, {'daily_review_time': '18:00'})
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.daily_review_time, time(18, 0))
    
    def test_view_shows_current_time(self):
        """Test that view displays current time setting"""
        self.profile.daily_review_time = time(12, 30)
        self.profile.save()
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        
        self.assertIn('current_time', response.context)
        self.assertEqual(response.context['current_time'], '12:30')

