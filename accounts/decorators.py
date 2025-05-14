# accounts/decorators.py
from django.contrib.auth.decorators import login_required, user_passes_test

def staff_or_admin_required(view_func):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.is_admin() or u.is_staff_member()),
        login_url='/accounts/login/'
    )
    return login_required(actual_decorator(view_func))