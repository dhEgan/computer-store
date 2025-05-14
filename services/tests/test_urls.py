from django.test import TestCase
from django.urls import reverse, resolve
from services import views

class UrlsTest(TestCase):
    def test_service_list_url(self):
        url = reverse('services:list')
        self.assertEqual(resolve(url).func, views.service_list)

    def test_service_detail_url(self):
        url = reverse('services:detail', kwargs={'slug': 'test-service'})
        self.assertEqual(resolve(url).func, views.service_detail)

    def test_service_search_url(self):
        url = reverse('services:search')
        self.assertEqual(resolve(url).func, views.service_search)