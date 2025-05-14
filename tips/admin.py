from django.contrib import admin
from .models import BeautyTip, BeautyTipCategory
from django.utils.html import format_html

class BeautyTipCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}  
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Mô tả'

class BeautyTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'created_at', 'views', 'image_preview')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'content', 'image')
        }),
        ('Tính năng', {
            'fields': ('is_featured', 'views')
        }),
        ('Ngày tháng', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "Không có ảnh"
    image_preview.short_description = 'Ảnh xem trước'

admin.site.register(BeautyTipCategory, BeautyTipCategoryAdmin)
admin.site.register(BeautyTip, BeautyTipAdmin)