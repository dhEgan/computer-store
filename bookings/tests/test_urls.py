from django.test import TestCase
from django.urls import reverse, resolve
from bookings import views

class UrlsTest(TestCase):
    def test_book_now_url(self):
        url = reverse('bookings:book_now')
        self.assertEqual(resolve(url).func, views.book_now)

    def test_booking_detail_url(self):
        url = reverse('bookings:booking_detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, views.booking_detail)

    def test_booking_history_url(self):
        url = reverse('bookings:history')
        self.assertEqual(resolve(url).func, views.booking_history)

    def test_cancel_booking_url(self):
        url = reverse('bookings:cancel_booking', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, views.cancel_booking)

    def test_admin_booking_list_url(self):
        url = reverse('bookings:admin_booking_list')
        self.assertEqual(resolve(url).func, views.admin_booking_list)

    def test_admin_booking_calendar_url(self):
        url = reverse('bookings:admin_booking_calendar')
        self.assertEqual(resolve(url).func, views.admin_booking_calendar)