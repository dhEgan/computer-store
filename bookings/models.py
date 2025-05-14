from django.db import models
from accounts.models import CustomUser
from services.models import Service
from django.core.validators import MinValueValidator
from django.utils import timezone
class Booking(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    points_awarded = models.BooleanField(default=False, verbose_name="Đã cộng điểm")
    points_awarded_date = models.DateTimeField(null=True, blank=True)

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        ordering = ['-booking_date']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        permissions = [
            ('manage_booking', 'Can manage all bookings'),
        ]

    def is_upcoming(self):
        return self.booking_date > timezone.now() and self.status in ['pending', 'confirmed']        

    def __str__(self):
        return f"{self.customer.username} - {self.service.name}"
    
    def get_status_class(self):
        return {
            'pending': 'warning',
            'confirmed': 'info',
            'completed': 'success',
            'cancelled': 'danger'
        }.get(self.status, 'secondary')