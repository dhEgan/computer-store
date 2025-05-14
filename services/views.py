from django.shortcuts import render
from .models import Service
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Service, ServiceReview, ServiceCategory
from .forms import ServiceReviewForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView


def home(request):
    services = Service.objects.all()[:4]
    return render(request, 'home.html', {'services': services})

def service_list(request):
    service_list = Service.objects.all()
    paginator = Paginator(service_list, 6)  
    
    page_number = request.GET.get('page')
    services = paginator.get_page(page_number)
    
    return render(request, 'services/list.html', {'services': services})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'services/detail.html', {'service': service})

def service_search(request):
    query = request.GET.get('q', '')
    services = Service.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    ).distinct()
    
    return render(request, 'services/search_results.html', {
        'services': services,
        'query': query
    })

@login_required
def add_review(request, slug):
   
    service = get_object_or_404(Service, slug=slug)
    
   
    existing_review = ServiceReview.objects.filter(
        service=service, 
        user=request.user
    ).first()
    
    if existing_review:
        messages.warning(request, 'Bạn đã đánh giá dịch vụ này trước đây.')
        return redirect('services:detail', slug=service.slug)
    
    if request.method == 'POST':
        form = ServiceReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.service = service
            review.user = request.user
            review.save()
            
            
            update_service_rating(service)
            
            messages.success(request, 'Cảm ơn bạn đã đánh giá dịch vụ!')
            return redirect('services:detail', slug=service.slug)
    else:
        form = ServiceReviewForm()
    
    context = {
        'service': service,
        'form': form,
        'review': existing_review,
    }
    return render(request, 'services/add_review.html', context)

def update_service_rating(service):
   
    reviews = service.reviews.all()
    if reviews.exists():
        total_rating = sum([review.rating for review in reviews])
        average_rating = total_rating / reviews.count()
        service.average_rating = round(average_rating, 1)
        service.review_count = reviews.count()
        service.save()


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin():
            return render(request, 'admin/access_denied.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def admin_service_list(request):
    services = Service.objects.all().order_by('-created_at')
    return render(request, 'admin/services/list.html', {'services': services})

@admin_required
def admin_service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    reviews = service.reviews.all().order_by('-created_at')[:10]
    return render(request, 'admin/services/detail.html', {
        'service': service,
        'reviews': reviews
    })



class AdminServiceCategoryCreateView(SuccessMessageMixin, CreateView):
    model = ServiceCategory
    fields = ['name', 'description', 'icon']
    template_name = 'admin/services/categories/form.html'
    success_message = "Category created successfully"
    success_url = reverse_lazy('services:admin_service_category_list')

class AdminServiceCategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = ServiceCategory
    fields = ['name', 'description', 'icon']
    template_name = 'admin/services/categories/form.html'
    success_message = "Category updated successfully"
    success_url = reverse_lazy('services:admin_service_category_list')


class AdminServiceCreateView(SuccessMessageMixin, CreateView):
    model = Service
    fields = ['category', 'name', 'description', 'price', 'duration', 'image', 'is_featured']
    template_name = 'admin/services/form.html'
    success_message = "Service created successfully"
    success_url = reverse_lazy('services:admin_service_list')

class AdminServiceUpdateView(SuccessMessageMixin, UpdateView):
    model = Service
    fields = ['category', 'name', 'description', 'price', 'duration', 'image', 'is_featured']
    template_name = 'admin/services/form.html'
    success_message = "Service updated successfully"
    
    def get_success_url(self):
        return reverse('services:admin_service_detail', kwargs={'pk': self.object.pk})

@admin_required
def admin_service_review_list(request, pk):
    service = get_object_or_404(Service, pk=pk)
    reviews = service.reviews.all().order_by('-created_at')
    return render(request, 'admin/services/reviews/list.html', {
        'service': service,
        'reviews': reviews
    })


class AdminServiceCategoryListView(LoginRequiredMixin, ListView):
    model = ServiceCategory
    template_name = 'admin/services/categories/list.html'
    context_object_name = 'categories'

class AdminServiceCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = ServiceCategory
    template_name = 'admin/services/categories/confirm_delete.html'
    success_url = reverse_lazy('services:admin_service_category_list')
    success_message = "Category deleted successfully"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
    

class AdminServiceDeleteView(SuccessMessageMixin, DeleteView):
    model = Service
    template_name = 'admin/services/confirm_delete.html'
    success_url = reverse_lazy('services:admin_service_list')
    success_message = "Service deleted successfully"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

@admin_required
def admin_review_detail(request, pk):
    review = get_object_or_404(ServiceReview, pk=pk)
    return render(request, 'admin/services/reviews/detail.html', {
        'review': review
    })