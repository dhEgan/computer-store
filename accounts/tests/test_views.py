from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from accounts.models import LoyaltyPoints, Voucher

CustomUser = get_user_model()

class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.admin = CustomUser.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com',
            user_type='admin'
        )

    def test_register_view(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_login_view(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:user_logout'))
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)

    def test_change_password_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:change_password'))
        self.assertEqual(response.status_code, 200)

class LoyaltyViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.points = LoyaltyPoints.objects.get(user=self.user)
        self.points.points = 100  
        self.points.save()
        
        self.voucher = Voucher.objects.create(
            user=self.user,
            code='TEST123',
            discount_percent=20,
            expires_at=timezone.now() + timedelta(days=30)
        )

    def test_loyalty_points_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:loyalty_points'))
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, '100')  
        self.assertContains(response, 'TEST123') 

    def test_redeem_points(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('accounts:loyalty_points'),
            {'redeem_points': True},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.points.refresh_from_db()
        self.assertEqual(self.points.points, 50)
        self.assertEqual(Voucher.objects.count(), 2)

class AdminViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = CustomUser.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com',
            user_type='admin'
        )
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_admin_dashboard(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('accounts:admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_admin_user_list(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('accounts:admin_user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_admin_user_detail(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(
            reverse('accounts:admin_user_detail', kwargs={'pk': self.user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)