from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from datetime import timedelta
from services.models import Service, ServiceCategory, ServiceReview
from django.contrib.auth import get_user_model

User = get_user_model()

class ServiceCategoryModelTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name="Massage",
            description="Massage treatments"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Massage")
        self.assertTrue(self.category.slug)

    def test_slug_uniqueness(self):
       
        ServiceCategory.objects.create(
            name="Massage Therapy",
            description="Different category"
        )
        
        # Thử tạo category với slug trùng
        with self.assertRaises(IntegrityError):
            ServiceCategory.objects.create(
                name="Massage",
                description="Duplicate category",
                slug=self.category.slug
            )

class ServiceModelTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="Massage")
        self.service = Service.objects.create(
            name="Swedish Massage",
            category=self.category,
            description="Relaxing massage",
            price=500000,
            duration=timedelta(minutes=60)
        )

    def test_service_creation(self):
        self.assertEqual(self.service.name, "Swedish Massage")
        self.assertEqual(self.service.price, 500000)
        self.assertTrue(self.service.slug)

    def test_duration_in_minutes(self):
        self.assertEqual(self.service.duration_in_minutes(), 60)

    def test_get_absolute_url(self):
        url = self.service.get_absolute_url()
        self.assertTrue(url.startswith('/services/'))