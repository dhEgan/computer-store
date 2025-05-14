from django.urls import path
from . import views
from .views import (
    book_now, booking_detail, booking_history, cancel_booking,
    admin_booking_list, AdminBookingDetailView, AdminBookingUpdateView,
    admin_booking_calendar
)


app_name = 'bookings'

urlpatterns = [
    path('', views.book_now, name='book_now'),
    path('<int:pk>/', views.booking_detail, name='booking_detail'),
    path('<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('history/', views.booking_history, name='history'),

    # Admin URLs
    path('admin/', admin_booking_list, name='admin_booking_list'),
    path('admin/<int:pk>/', AdminBookingDetailView.as_view(), name='admin_booking_detail'),
    path('admin/<int:pk>/edit/', AdminBookingUpdateView.as_view(), name='admin_booking_update'),
    path('admin/calendar/', admin_booking_calendar, name='admin_booking_calendar'),
]