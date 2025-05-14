from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def is_admin(self):
        return self.user_type == 'admin'
    
    def is_staff_member(self):
        return self.user_type == 'staff'
    
    def is_customer(self):
        return self.user_type == 'customer'
    




class LoyaltyPoints(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='loyalty_points')
    points = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Loyalty Points"
        managed = False  

    def __str__(self):
        return f"{self.user.username} - {self.points} points"

class Voucher(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='vouchers')
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.code} - {self.discount_percent}% off"

@receiver(post_save, sender=CustomUser)
def create_user_loyalty_points(sender, instance, created, **kwargs):
    if created:
        LoyaltyPoints.objects.create(user=instance)
    
    