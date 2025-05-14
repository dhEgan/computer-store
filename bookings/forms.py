from django import forms
from .models import Booking
from services.models import Service
from django.utils import timezone
from datetime import datetime, time

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'booking_date', 'notes']
        widgets = {
            'booking_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Nhập ghi chú của bạn...',}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_authenticated:
            self.fields['service'].queryset = Service.objects.all()
        
    
        now = timezone.now()
        min_date = now.strftime('%Y-%m-%d')
        min_time = now.strftime('%H:%M')
        self.fields['booking_date'].widget.attrs.update({
            'min': min_date,
            'value': min_date + 'T' + min_time
        })
    
    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date < timezone.now():
            raise forms.ValidationError("Thời gian đặt lịch không thể trong quá khứ!")
        return booking_date