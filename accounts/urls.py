from django.urls import path
from .views import (
    register,
    user_login,
    user_logout,
    profile,
    change_password,
    admin_dashboard,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView, 
    admin_user_list, 
    admin_user_detail,AdminUserCreateView,
    AdminUserUpdateView, AdminUserDeleteView,
    manage_points
)
from . import views
from .views import loyalty_points
from accounts.views import manage_points

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('profile/', profile, name='profile'),
    path('password-reset/', 
         CustomPasswordResetView.as_view(), 
         name='password_reset'),
    path('password-reset/done/', 
         CustomPasswordResetDoneView.as_view(), 
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    path('password-reset/complete/',
         CustomPasswordResetCompleteView.as_view(), 
         name='password_reset_complete'),
    path('change-password/', change_password, name='change_password'),
    path('booking-history/', views.booking_history, name='booking_history'),
    path('loyalty-points/', loyalty_points, name='loyalty_points'),
    path('admin/manage-points/', manage_points, name='manage_points'),

    # Admin URLs
    path('admin/', admin_dashboard, name='admin_dashboard'),
    
    # User management
    path('admin/users/', admin_user_list, name='admin_user_list'),
    path('admin/users/create/', AdminUserCreateView.as_view(), name='admin_user_create'),
    path('admin/users/<int:pk>/', admin_user_detail, name='admin_user_detail'),
    path('admin/users/<int:pk>/edit/', AdminUserUpdateView.as_view(), name='admin_user_update'),
    path('admin/users/<int:pk>/delete/', AdminUserDeleteView.as_view(), name='admin_user_delete'),
    
    # Loyalty
    path('admin/loyalty-points/', manage_points, name='manage_points'),
    # URL cho Staff
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/bookings/<int:pk>/', views.staff_booking_detail, name='staff_booking_detail'),
]