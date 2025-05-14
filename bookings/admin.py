from django.contrib import admin
from .models import Booking
from django.utils.html import format_html
from django.db.models import F
from accounts.models import LoyaltyPoints
from django.utils import timezone

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'booking_date', 'status_badge', 'created_at', 'points_awarded')
    list_filter = ('status', 'service', 'booking_date', 'points_awarded')
    search_fields = ('customer__username', 'customer__email', 'service__name')
    readonly_fields = ('created_at', 'points_awarded_date')
    date_hierarchy = 'booking_date'
    actions = ['confirm_bookings', 'cancel_bookings', 'complete_bookings']

    fieldsets = (
        (None, {
            'fields': ('customer', 'service', 'booking_date')
        }),
        ('Status', {
            'fields': ('status', 'notes', 'points_awarded', 'points_awarded_date')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'green',
            'completed': 'blue',
            'cancelled': 'red'
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 2px 6px; border-radius: 4px;">{}</span>',
            colors[obj.status],
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'

    def confirm_bookings(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'{updated} bookings confirmed.')
    confirm_bookings.short_description = "Confirm selected bookings"

    def cancel_bookings(self, request, queryset):
        updated = queryset.exclude(status='cancelled').update(status='cancelled')
        self.message_user(request, f'{updated} bookings cancelled.')
    cancel_bookings.short_description = "Cancel selected bookings"

    def complete_bookings(self, request, queryset):
        completed_count = 0
        for booking in queryset.filter(status='confirmed'):
            
            if not booking.points_awarded:
                booking.status = 'completed'
                booking.points_awarded = True
                booking.points_awarded_date = timezone.now()
                booking.save()
                
                
                points, created = LoyaltyPoints.objects.get_or_create(
                    user=booking.customer,
                    defaults={'points': 10}
                )
                if not created:
                    points.points += 10
                    points.save()
                
                completed_count += 1
        
        self.message_user(
            request, 
            f'Đã hoàn thành {completed_count} booking và cộng điểm. '
            f'{queryset.count() - completed_count} booking đã được bỏ qua (đã hoàn thành hoặc đã được cộng điểm trước đó).'
        )
    complete_bookings.short_description = "Đánh dấu đã hoàn thành và cộng điểm"


