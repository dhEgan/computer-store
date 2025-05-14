from django.test import TestCase, Client
from django.urls import reverse
from services.models import Service, ServiceCategory
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

class ServiceViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = ServiceCategory.objects.create(name="Massage")
        self.service = Service.objects.create(
            name="Test Service",
            category=self.category,
            description="Test description",
            price=300000,
            duration=timedelta(minutes=30)
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_service_list_view(self):
        response = self.client.get(reverse('services:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Service")
        self.assertTemplateUsed(response, 'services/list.html')

    def test_service_detail_view(self):
        response = self.client.get(
            reverse('services:detail', kwargs={'slug': self.service.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test description")

    def test_service_search_view(self):
        response = self.client.get(
            reverse('services:search') + '?q=Test'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Service")

    def test_add_review_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('services:add_review', kwargs={'slug': self.service.slug}),
            {'rating': 5, 'comment': 'Great service!'}
        )
        self.assertEqual(response.status_code, 302) 

    def test_add_review_unauthenticated(self):
        response = self.client.get(
            reverse('services:add_review', kwargs={'slug': self.service.slug})
        )
        self.assertEqual(response.status_code, 302) 