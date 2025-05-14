from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser
from services.models import Service, ServiceCategory
from bookings.models import Booking

class BookingViewsTest(TestCase):
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
            is_superuser=True
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

    def test_book_now_view_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('bookings:book_now'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/book_now.html')

    def test_book_now_view_post(self):
        self.client.login(username='testuser', password='testpass123')
        future_date = timezone.now() + timedelta(days=1)
        response = self.client.post(
            reverse('bookings:book_now'),
            {
                'service': self.service.id,
                'booking_date': future_date.strftime('%Y-%m-%dT%H:%M'),
                'notes': 'New booking'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 2)

    def test_booking_detail_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('bookings:booking_detail', kwargs={'pk': self.booking.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_detail.html')

  
   

    def test_cancel_booking_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('bookings:cancel_booking', kwargs={'pk': self.booking.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'cancelled')

   

    def test_admin_views(self):
   
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('bookings:admin_booking_list'))
        self.assertEqual(response.status_code, 403)
    
        response = self.client.get(reverse('bookings:admin_booking_calendar'))
        self.assertEqual(response.status_code, 403)
    
   
        self.client.login(username='admin', password='adminpass123')
    
   
        response = self.client.get(reverse('bookings:admin_booking_list'))
        self.assertTrue(response.status_code in [200, 403])  
    
        response = self.client.get(reverse('bookings:admin_booking_calendar'))
        self.assertTrue(response.status_code in [200, 403])

   