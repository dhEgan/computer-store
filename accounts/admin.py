from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LoyaltyPoints, Voucher  
from bookings.models import Booking
from django.utils import timezone

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)



@admin.register(LoyaltyPoints)
class LoyaltyPointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'last_updated', 'get_completed_bookings')
    search_fields = ('user__username', 'user__email')
    list_filter = ('last_updated',)
    list_select_related = ('user',)
    
    def get_completed_bookings(self, obj):
        """Hiển thị số booking đã hoàn thành của user"""
        return Booking.objects.filter(
            customer=obj.user, 
            status='completed',
            points_awarded=True
        ).count()
    get_completed_bookings.short_description = 'Số dịch vụ đã hoàn thành'

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.unregister(LoyaltyPoints)
