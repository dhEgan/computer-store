from django.contrib import admin
from .models import ServiceCategory, Service, ServiceReview
from django.utils.html import format_html

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration_in_minutes', 'is_featured', 'average_rating')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'average_rating', 'review_count')
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'duration')
        }),
        ('Media', {
            'fields': ('image', 'is_featured')
        }),
        ('Ratings', {
            'fields': ('average_rating', 'review_count')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def duration_in_minutes(self, obj):
        return obj.duration_in_minutes()
    duration_in_minutes.short_description = 'Duration (min)'

class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'rating_stars', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('service__name', 'user__username', 'comment')
    readonly_fields = ('created_at', 'updated_at')

    def rating_stars(self, obj):
        return obj.get_rating_stars()
    rating_stars.short_description = 'Rating'

admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceReview, ServiceReviewAdmin)
