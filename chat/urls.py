# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chuyen-vien/', views.chat_expert, name='expert'),
]
