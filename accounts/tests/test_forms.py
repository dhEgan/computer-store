from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.forms import CustomUserCreationForm, ProfileForm

CustomUser = get_user_model()

class CustomUserCreationFormTest(TestCase):
    def test_valid_registration_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpassword123',
            'password2': 'differentpassword'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

class ProfileFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_valid_profile_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'address': '123 Main St'
        }
        form = ProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email',
            'phone': '1234567890'
        }
        form = ProfileForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)