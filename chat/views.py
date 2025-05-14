# views.py
from django.shortcuts import render

def chat_expert(request):
    return render(request, 'chat/chat_expert.html')
