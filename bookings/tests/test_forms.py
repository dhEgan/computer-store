from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser
from services.models import Service, ServiceCategory
from bookings.forms import BookingForm
from bookings.models import Booking

class BookingFormTest(TestCase):
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

    def test_valid_booking_form(self):
        future_date = timezone.now() + timedelta(days=1)
        form_data = {
            'service': self.service.id,
            'booking_date': future_date.strftime('%Y-%m-%dT%H:%M'),
            'notes': 'Test booking'
        }
        form = BookingForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_past_date_validation(self):
        past_date = timezone.now() - timedelta(days=1)
        form_data = {
            'service': self.service.id,
            'booking_date': past_date.strftime('%Y-%m-%dT%H:%M'),
            'notes': 'Test booking'
        }
        form = BookingForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('booking_date', form.errors)
        self.assertEqual(
            form.errors['booking_date'][0],
            "Thời gian đặt lịch không thể trong quá khứ!"
        )

    def test_form_initialization(self):
        form = BookingForm(user=self.user)
        self.assertEqual(
            form.fields['service'].queryset.count(),
            1
        )
        self.assertEqual(
            form.fields['service'].queryset.first(),
            self.service
        )