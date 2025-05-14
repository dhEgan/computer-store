from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'user_type']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'user_type': forms.Select(choices=CustomUser.USER_TYPE_CHOICES),
        }