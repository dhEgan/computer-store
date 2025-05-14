from django.test import TestCase
from django.template import Template, Context
from services.models import Service, ServiceCategory

class TemplateTagsTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="Massage")
        self.service = Service.objects.create(
            name="Test Service",
            category=self.category,
            description="Test description",
            price=300000,
            duration=30
        )

    def test_service_card_template(self):
        template = Template("""
            {% load static %}
            {% for service in services %}
                <div class="service-card">
                    <h3>{{ service.name }}</h3>
                    <p>{{ service.description }}</p>
                </div>
            {% endfor %}
        """)
        context = Context({'services': [self.service]})
        rendered = template.render(context)
        self.assertIn("Test Service", rendered)
        self.assertIn("Test description", rendered)