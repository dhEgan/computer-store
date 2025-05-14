from django.test import TestCase
from django.urls import reverse, resolve
from accounts import views

class UrlsTest(TestCase):
    def test_register_url(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func, views.register)

    def test_login_url(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func, views.user_login)

    def test_profile_url(self):
        url = reverse('accounts:profile')
        self.assertEqual(resolve(url).func, views.profile)

    def test_loyalty_points_url(self):
        url = reverse('accounts:loyalty_points')
        self.assertEqual(resolve(url).func, views.loyalty_points)

    def test_admin_dashboard_url(self):
        url = reverse('accounts:admin_dashboard')
        self.assertEqual(resolve(url).func, views.admin_dashboard)

    def test_admin_user_list_url(self):
        url = reverse('accounts:admin_user_list')
        self.assertEqual(resolve(url).func, views.admin_user_list)