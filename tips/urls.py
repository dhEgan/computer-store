from django.urls import path
from . import views
from .views import admin_tip_list,admin_tip_category_list , AdminTipCreateView,AdminTipUpdateView,AdminTipDeleteView,AdminTipCategoryCreateView,AdminTipCategoryUpdateView, AdminTipCategoryDeleteView

app_name = 'tips'

urlpatterns = [
    path('', views.tip_list, name='list'),
    path('admin/', admin_tip_list , name='admin_tip_list'),
    path('admin/categories/', admin_tip_category_list, name='admin_tip_category_list'),
    path('admin/categories/create/', AdminTipCategoryCreateView.as_view(), name='admin_tip_category_create'),
    path('admin/categories/update/<int:pk>/', AdminTipCategoryUpdateView.as_view(), name='admin_tip_category_update'),
    path('admin/categories/delete/<int:pk>/', AdminTipCategoryDeleteView.as_view(), name='admin_tip_category_delete'),
    path('admin/tips/create', AdminTipCreateView.as_view(), name='admin_tip_create'),
    path('admin/tips/update/<int:pk>/', AdminTipUpdateView.as_view(), name='admin_tip_update'),
    path('admin/delete/<int:pk>/', AdminTipDeleteView.as_view(), name='admin_tip_delete'),
    path('category/<slug:slug>/', views.tip_category, name='category'),
    path('<slug:slug>/', views.tip_detail, name='detail'),

    
    # path('tag/<slug:slug>/', views.tip_tag, name='tag'),
    
]