from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookingForm
from services.models import Service
from .models import Booking
from django.utils import timezone 
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin():
            return render(request, 'admin/access_denied.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)
@login_required
def book_now(request):
    service_id = request.GET.get('service', None)
    try:
        initial_service = get_object_or_404(Service, pk=service_id) if service_id else None
    except Exception as e:
        logger.error(f"Error fetching service {service_id}: {str(e)}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': f'Invalid service ID: {str(e)}'}, status=400)
        messages.error(request, 'Dịch vụ không hợp lệ.')
        return render(request, 'bookings/book_now.html', {'form': BookingForm(user=request.user)})
    
    try:
        if request.method == 'POST':
            logger.debug(f"POST data: {request.POST}")
            form = BookingForm(request.POST, user=request.user)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.customer = request.user
                booking.save()
                logger.info(f"Booking created: ID {booking.pk}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'booking_id': booking.pk})
                messages.success(request, 'Đặt lịch thành công! Chúng tôi sẽ liên hệ với bạn sớm.')
                return redirect('bookings:booking_detail', pk=booking.pk)
            else:
                logger.warning(f"Form errors: {form.errors}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': form.errors.as_text()}, status=400)
                messages.error(request, 'Dữ liệu không hợp lệ. Vui lòng kiểm tra lại.')
                return render(request, 'bookings/book_now.html', {
                    'form': form,
                    'services': Service.objects.all(),
                    'selected_service': initial_service
                })
        else:
            form = BookingForm(user=request.user, initial={'service': initial_service})
        
        services = Service.objects.all()
        return render(request, 'bookings/book_now.html', {
            'form': form,
            'services': services,
            'selected_service': initial_service
        })
    except Exception as e:
        logger.error(f"Server error in book_now: {str(e)}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'}, status=500)
        messages.error(request, 'Có lỗi xảy ra. Vui lòng thử lại.')
        return render(request, 'bookings/book_now.html', {
            'form': BookingForm(user=request.user),
            'services': Service.objects.all()
        })
@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.customer != request.user and not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền xem đặt lịch này.')
        return redirect('home')
    
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-booking_date')
    return render(request, 'bookings/history.html', {'bookings': bookings})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    
    if booking.customer != request.user and not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền hủy đặt lịch này.')
        return redirect('bookings:booking_history')
    
    
    if booking.is_upcoming() and booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Đã hủy đặt lịch thành công.')
    else:
        messages.error(request, 'Không thể hủy đặt lịch này.')
    
    return redirect('bookings:booking_detail', pk=booking.pk)


@admin_required
def admin_booking_list(request):
    status_filter = request.GET.get('status', 'all')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    bookings = Booking.objects.all().order_by('-booking_date')
    
    if status_filter != 'all':
        bookings = bookings.filter(status=status_filter)
    
    if date_from:
        bookings = bookings.filter(booking_date__gte=date_from)
    
    if date_to:
        bookings = bookings.filter(booking_date__lte=date_to)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'date_from': date_from,
        'date_to': date_to,
        'status_choices': Booking.STATUS_CHOICES,
    }
    return render(request, 'admin/bookings/list.html', context)

class AdminBookingDetailView(DetailView):
    model = Booking
    template_name = 'admin/bookings/detail.html'
    context_object_name = 'booking'

class AdminBookingUpdateView(SuccessMessageMixin, UpdateView):
    model = Booking
    fields = ['status', 'notes']
    template_name = 'admin/bookings/form.html'
    success_message = "Booking updated successfully"
    
    def get_success_url(self):
        return reverse('bookings:admin_booking_detail', kwargs={'pk': self.object.pk})

@admin_required
def admin_booking_calendar(request):
    bookings = Booking.objects.filter(
        booking_date__gte=timezone.now()
    ).order_by('booking_date')
    
    events = []
    for booking in bookings:
        events.append({
            'title': f"{booking.customer.get_short_name()} - {booking.service.name}",
            'start': booking.booking_date.isoformat(),
            'end': (booking.booking_date + booking.service.duration).isoformat(),
            'className': f'bg-{booking.get_status_class()}',
            'url': reverse('bookings:admin_booking_detail', kwargs={'pk': booking.pk}),
        })
    
    return render(request, 'admin/bookings/calendar.html', {
        'events': events
    })