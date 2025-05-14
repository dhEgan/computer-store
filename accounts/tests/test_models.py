from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from accounts.models import LoyaltyPoints, Voucher

CustomUser = get_user_model()

class CustomUserModelTest(TestCase):
    def setUp(self):
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

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.user_type, 'customer')
        self.assertFalse(self.user.is_admin())
        self.assertTrue(self.user.is_customer())

    def test_admin_creation(self):
        self.assertEqual(self.admin.username, 'admin')
        self.assertEqual(self.admin.user_type, 'admin')
        self.assertTrue(self.admin.is_admin())
        self.assertFalse(self.admin.is_customer())

    def test_loyalty_points_creation_signal(self):
       
        points = LoyaltyPoints.objects.filter(user=self.user).first()
        self.assertIsNotNone(points)
        self.assertEqual(points.points, 0)

class LoyaltyPointsModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.points = LoyaltyPoints.objects.get(user=self.user)
        self.points.points = 100  
        self.points.save()

    def test_loyalty_points_creation(self):
        self.assertEqual(self.points.user.username, "testuser")
        self.assertEqual(self.points.points, 100)
        self.assertEqual(str(self.points), 'testuser - 100 points')

class VoucherModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.voucher = Voucher.objects.create(
            user=self.user,
            code='TEST123',
            discount_percent=20,
            expires_at=timezone.now() + timedelta(days=30)
        )

    def test_voucher_creation(self):
        self.assertEqual(self.voucher.user.username, 'testuser')
        self.assertEqual(self.voucher.code, 'TEST123')
        self.assertEqual(self.voucher.discount_percent, 20)
        self.assertFalse(self.voucher.is_used)
        self.assertEqual(
            str(self.voucher),
            f"TEST123 - 20% off"
        )