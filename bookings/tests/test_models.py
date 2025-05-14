from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser
from services.models import Service, ServiceCategory
from bookings.models import Booking

class BookingModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        self.category = ServiceCategory.objects.create(
            name="Massage",
            description="Massage treatments"
        )
        
        self.service = Service.objects.create(
            name="Swedish Massage",
            category=self.category,
            description="Relaxing massage",
            price=500000,
            duration=timedelta(minutes=60)
        )
        
        self.booking = Booking.objects.create(
            customer=self.user,
            service=self.service,
            booking_date=timezone.now() + timedelta(days=1),
            notes="Test booking"
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.customer.username, "testuser")
        self.assertEqual(self.booking.service.name, "Swedish Massage")
        self.assertEqual(self.booking.status, "pending")

    def test_is_upcoming(self):
       
        self.assertTrue(self.booking.is_upcoming())
        
        
        past_booking = Booking.objects.create(
            customer=self.user,
            service=self.service,
            booking_date=timezone.now() - timedelta(days=1),
            notes="Past booking"
        )
        self.assertFalse(past_booking.is_upcoming())

    def test_get_status_class(self):
        self.assertEqual(self.booking.get_status_class(), "warning")
        
        self.booking.status = "confirmed"
        self.assertEqual(self.booking.get_status_class(), "info")
        
        self.booking.status = "completed"
        self.assertEqual(self.booking.get_status_class(), "success")
        
        self.booking.status = "cancelled"
        self.assertEqual(self.booking.get_status_class(), "danger")

    def test_str_representation(self):
        self.assertEqual(
            str(self.booking),
            f"{self.user.username} - {self.service.name}"
        )