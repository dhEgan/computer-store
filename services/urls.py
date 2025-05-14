from django.urls import path
from . import views

from .views import (
    admin_service_list,
    admin_service_detail,AdminServiceCreateView,
    AdminServiceUpdateView, AdminServiceDeleteView,
    AdminServiceCategoryListView, AdminServiceCategoryCreateView,
    AdminServiceCategoryUpdateView, AdminServiceCategoryDeleteView,
    admin_service_review_list,admin_review_detail
)

app_name = 'services'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.service_list, name='list'),
    path('search/', views.service_search, name='search'),
    path('<slug:slug>/', views.service_detail, name='detail'),
    path('<slug:slug>/review/', views.add_review, name='add_review'),

    # Service management
    path('admin/services/', admin_service_list, name='admin_service_list'),
    path('admin/services/create/', AdminServiceCreateView.as_view(), name='admin_service_create'),
    path('admin/services/<int:pk>/', admin_service_detail, name='admin_service_detail'),
    path('admin/services/<int:pk>/edit/', AdminServiceUpdateView.as_view(), name='admin_service_update'),
    path('admin/services/<int:pk>/delete/', AdminServiceDeleteView.as_view(), name='admin_service_delete'),
    path('admin/services/<int:pk>/reviews/', admin_service_review_list, name='admin_service_reviews'),
    path('admin/reviews/<int:pk>/', admin_review_detail, name='admin_review_detail'),
    
    # Category management
    path('admin/service-categories/', AdminServiceCategoryListView.as_view(), name='admin_service_category_list'),
    path('admin/service-categories/create/', AdminServiceCategoryCreateView.as_view(), name='admin_service_category_create'),
    path('admin/service-categories/<int:pk>/edit/', AdminServiceCategoryUpdateView.as_view(), name='admin_service_category_update'),
    path('admin/service-categories/<int:pk>/delete/', AdminServiceCategoryDeleteView.as_view(), name='admin_service_category_delete'),
]