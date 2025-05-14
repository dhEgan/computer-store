from django.test import TestCase
from services.forms import ServiceReviewForm
from services.models import Service, ServiceCategory
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

class ServiceReviewFormTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="Massage")
        self.service = Service.objects.create(
            name="Test Service",
            category=self.category,
            description="Test",
            price=300000,
            duration=timedelta(minutes=30)
        )
        self.user = User.objects.create_user(username='testuser')

    def test_valid_review_form(self):
        form_data = {
            'rating': 5,
            'comment': 'Excellent service'
        }
        form = ServiceReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_rating(self):
        form_data = {
            'rating': 6,  
            'comment': 'Test comment'
        }
        form = ServiceReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)