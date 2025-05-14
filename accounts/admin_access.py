from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import Http404

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin():
            return render(request, 'admin/access_denied.html', status=404)
        return view_func(request, *args, **kwargs)
    return wrapper