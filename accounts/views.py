from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.shortcuts import redirect
from services.models import Service, ServiceReview
from django.db.models import Count, Q
from datetime import datetime, timedelta
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth import update_session_auth_hash 
from bookings.models import Booking
from django.shortcuts import render, redirect, get_object_or_404
from .models import LoyaltyPoints, Voucher
from django.utils import timezone
from accounts.models import CustomUser
from django.db.models import Sum
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from .decorators import staff_or_admin_required


def admin_required(view_func):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_admin(),
        login_url='/accounts/login/'
    )
    return login_required(actual_decorator(view_func))

@admin_required
def admin_dashboard(request):
    
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    
    total_services = Service.objects.count()
    featured_services = Service.objects.filter(is_featured=True).count()
    
    
    total_reviews = ServiceReview.objects.count()
    recent_reviews = ServiceReview.objects.filter(created_at__date__gte=week_ago).count()
    
    
    from accounts.models import CustomUser
    total_users = CustomUser.objects.count()
    new_users = CustomUser.objects.filter(date_joined__date__gte=week_ago).count()
    
    
    popular_services = Service.objects.annotate(
        review_count=Count('reviews')
    ).order_by('-review_count')[:5]
    
    
    recent_review_list = ServiceReview.objects.select_related('service', 'user').order_by('-created_at')[:5]
    
    context = {
        'total_services': total_services,
        'featured_services': featured_services,
        'total_reviews': total_reviews,
        'recent_reviews': recent_reviews,
        'total_users': total_users,
        'new_users': new_users,
        'popular_services': popular_services,
        'recent_review_list': recent_review_list,
    }
    
    return render(request, 'admin/dashboard.html', context)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, 
            _('Chúng tôi đã gửi email hướng dẫn đặt lại mật khẩu. '
              'Nếu không thấy email, vui lòng kiểm tra thư mục spam.'))
        return response

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    
    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Exception as e:
            messages.error(self.request, _('Liên kết đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.'))
            return redirect('accounts:password_reset')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Mật khẩu của bạn đã được đặt lại thành công. Vui lòng đăng nhập với mật khẩu mới.'))
        return response

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

    def get(self, request, *args, **kwargs):
        messages.success(request, 
            _('Mật khẩu của bạn đã được thay đổi thành công. Bây giờ bạn có thể đăng nhập.'))
        return super().get(request, *args, **kwargs)
    

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Đăng ký tài khoản thành công!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Đăng nhập thành công!')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất thành công.')
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thông tin cá nhân đã được cập nhật!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Mật khẩu đã được thay đổi thành công!')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def booking_history(request):
    
    bookings = Booking.objects.filter(customer=request.user).order_by('-booking_date')
    return render(request, 'accounts/booking_history.html', {'bookings': bookings})



@login_required
def loyalty_points(request):
    points = get_object_or_404(LoyaltyPoints, user=request.user)
    vouchers = Voucher.objects.filter(user=request.user, is_used=False, expires_at__gte=timezone.now())
    
    if request.method == 'POST' and 'redeem_points' in request.POST:
        if points.points >= 50:
            
            voucher_code = f"VOUCHER-{request.user.id}-{int(timezone.now().timestamp())}"
            voucher = Voucher.objects.create(
                user=request.user,
                code=voucher_code,
                discount_percent=50,
                expires_at=timezone.now() + timedelta(days=30)
            )
            
            
            points.points -= 50
            points.save()
            
            messages.success(request, 'Bạn đã quy đổi thành công voucher giảm 50%!')
            return redirect('accounts:loyalty_points')
        else:
            messages.error(request, 'Bạn không đủ điểm để quy đổi voucher.')
    
    return render(request, 'accounts/loyalty_points.html', {
        'points': points,
        'vouchers': vouchers
    })


@login_required
@user_passes_test(lambda u: u.is_admin)
def manage_points(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id, status='completed')
        
        if not booking.points_awarded:
            points, created = LoyaltyPoints.objects.get_or_create(
                user=booking.customer,
                defaults={'points': 10}
            )
            
            if not created:
                points.points += 10
                points.save()
            
            booking.points_awarded = True
            booking.points_awarded_date = timezone.now()
            booking.save()
            messages.success(request, 'Đã cộng 10 điểm cho khách hàng')
            return redirect('accounts:manage_points')
    
    
    pending_bookings = Booking.objects.filter(
        status='completed',
        points_awarded=False
    ).select_related('customer', 'service')
    
    return render(request, 'admin/manage_points.html', {
        'pending_bookings': pending_bookings
    })


@admin_required
def admin_user_list(request):
    search_query = request.GET.get('q', '')
    
    users = CustomUser.objects.all().order_by('-date_joined')
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    paginator = Paginator(users, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'search_query': search_query,
    }
    return render(request, 'admin/users/list.html', context)

@admin_required
def admin_user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    bookings = Booking.objects.filter(customer=user).order_by('-booking_date')[:10]
    points = LoyaltyPoints.objects.filter(user=user).first()
    
    
    completed_bookings_count = Booking.objects.filter(customer=user, status='completed').count()
    active_vouchers_count = user.vouchers.filter(is_used=False, expires_at__gte=timezone.now()).count()

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully')
            return redirect('accounts:admin_user_detail', pk=user.pk)
    else:
        form = ProfileForm(instance=user)
    
    context = {
        'user': user,
        'form': form,
        'bookings': bookings,
        'points': points,
        'completed_bookings_count': completed_bookings_count,
        'active_vouchers_count': active_vouchers_count,
        'now': timezone.now(),
    }
    return render(request, 'admin/users/detail.html', context)


@admin_required
def admin_dashboard(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    
    total_users = CustomUser.objects.count()
    new_users_week = CustomUser.objects.filter(date_joined__date__gte=week_ago).count()
    user_growth = (new_users_week / total_users * 100) if total_users > 0 else 0
    
    
    total_bookings = Booking.objects.count()
    new_bookings_week = Booking.objects.filter(created_at__date__gte=week_ago).count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    
    
    revenue_month = Booking.objects.filter(
        created_at__date__gte=month_ago
    ).aggregate(total=Sum('service__price'))['total'] or 0
    
    
    recent_users = CustomUser.objects.order_by('-date_joined')[:5]
    recent_bookings = Booking.objects.select_related('customer', 'service').order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'new_users_week': new_users_week,
        'user_growth': round(user_growth, 1),
        'total_bookings': total_bookings,
        'new_bookings_week': new_bookings_week,
        'completed_bookings': completed_bookings,
        'revenue_month': revenue_month,
        'recent_users': recent_users,
        'recent_bookings': recent_bookings,
    }
    
    return render(request, 'admin/dashboard.html', context)



class AdminUserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'admin/users/form.html'
    success_message = "User created successfully"
    success_url = reverse_lazy('accounts:admin_user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        LoyaltyPoints.objects.create(user=self.object)
        return response


class AdminUserUpdateView(SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'admin/users/form.html'
    success_message = "User updated successfully"
    
    def get_success_url(self):
        return reverse('accounts:admin_user_detail', kwargs={'pk': self.object.pk})


class AdminUserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'admin/users/confirm_delete.html'
    success_url = reverse_lazy('accounts:admin_user_list')
    success_message = "User deleted successfully"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
    

@admin_required
def admin_voucher_list(request):
    status_filter = request.GET.get('status', 'active')
    
    vouchers = Voucher.objects.all().order_by('-created_at')
    
    if status_filter == 'active':
        vouchers = vouchers.filter(is_used=False, expires_at__gte=timezone.now())
    elif status_filter == 'expired':
        vouchers = vouchers.filter(expires_at__lt=timezone.now())
    elif status_filter == 'used':
        vouchers = vouchers.filter(is_used=True)
    
    context = {
        'vouchers': vouchers,
        'status_filter': status_filter,
    }
    return render(request, 'admin/vouchers/list.html', context)


@staff_or_admin_required
def staff_dashboard(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    # Dữ liệu cho Bảng Điều Khiển
    total_bookings = Booking.objects.count()
    new_bookings_week = Booking.objects.filter(created_at__date__gte=week_ago).count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    
    # Dữ liệu cho Quản lý Đặt Hàng
    bookings = Booking.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_bookings': total_bookings,
        'new_bookings_week': new_bookings_week,
        'completed_bookings': completed_bookings,
        'bookings': bookings,
    }
    
    return render(request, 'staff/dashboard.html', context)


@staff_or_admin_required
def staff_booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Booking.STATUS_CHOICES).keys():
            booking.status = status
            booking.save()
            messages.success(request, 'Cập nhật trạng thái đơn hàng thành công!')
            return redirect('accounts:staff_dashboard')
    
    context = {
        'booking': booking,
    }
    return render(request, 'staff/booking_detail.html', context)