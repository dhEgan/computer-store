from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from accounts.views import admin_required
from django.http import Http404

CustomUser = get_user_model()

class AdminRequiredDecoratorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin = CustomUser.objects.create_superuser(
            username='admin',
            password='adminpass123',
            user_type='admin'
        )

    def test_admin_access(self):
        request = self.factory.get('/admin/')
        request.user = self.admin
        
        @admin_required
        def test_view(request):
            return "OK"
        
        response = test_view(request)
        self.assertEqual(response, "OK")

    def test_non_admin_access(self):
        request = self.factory.get('/admin/')
        request.user = self.user
    
        @admin_required
        def test_view(request):
            return "OK"
    
        response = test_view(request)
        self.assertEqual(response.status_code, 302)