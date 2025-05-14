from django.shortcuts import render, get_object_or_404
from .models import BeautyTip
from django.core.paginator import Paginator
from .models import BeautyTip, BeautyTipCategory
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.utils.text import slugify


def admin_required(view_func):
   
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin():
            return render(request, 'admin/access_denied.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper

def tip_list(request):
    tip_list = BeautyTip.objects.all().order_by('-created_at')
    paginator = Paginator(tip_list, 8)  
    
    page_number = request.GET.get('page')
    tips = paginator.get_page(page_number)
    
    return render(request, 'tips/list.html', {'tips': tips})



def tip_detail(request, slug):
   
    tip = get_object_or_404(BeautyTip, slug=slug)
    
   
    tip.views += 1
    tip.save(update_fields=['views'])
    
    
    related_tips = BeautyTip.objects.filter(
        category=tip.category
    ).exclude(
        id=tip.id
    ).order_by('-created_at')[:4]
    
    
    featured_tips = BeautyTip.objects.filter(
        is_featured=True
    ).exclude(
        id=tip.id
    ).order_by('-created_at')[:3]
    
   
    popular_categories = BeautyTipCategory.objects.annotate(
        tip_count=Count('beautytip')
    ).order_by('-tip_count')[:5]
    
    context = {
        'tip': tip,
        'related_tips': related_tips,
        'featured_tips': featured_tips,
        'popular_categories': popular_categories,
    }
    
    return render(request, 'tips/detail.html', context)

def tip_category(request, slug):
    category = get_object_or_404(BeautyTipCategory, slug=slug)
    tips = BeautyTip.objects.filter(category=category).order_by('-created_at')
    
    context = {
        'category': category,
        'tips': tips,
    }
    return render(request, 'tips/category.html', context)


from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

@admin_required
def admin_tip_list(request):
    tips = BeautyTip.objects.all().order_by('-created_at')
    return render(request, 'admin/tips/list.html', {'tips': tips})

class AdminTipCreateView(SuccessMessageMixin, CreateView):
    model = BeautyTip
    fields = ['category', 'title', 'content', 'image', 'is_featured']
    template_name = 'admin/tips/form.html'
    success_message = "Beauty tip created successfully"
    success_url = reverse_lazy('tips:admin_tip_list')

    def form_valid(self, form):
        if form.instance.title:
            if not form.instance.slug:
                form.instance.slug = slugify(form.instance.title)
        
        return super().form_valid(form)

class AdminTipUpdateView(SuccessMessageMixin, UpdateView):
    model = BeautyTip
    fields = ['category', 'title', 'content', 'image', 'is_featured']
    template_name = 'admin/tips/form.html'
    success_message = "Beauty tip updated successfully"
    success_url = reverse_lazy('tips:admin_tip_list')

@admin_required
def admin_tip_category_list(request):
    categories = BeautyTipCategory.objects.annotate(
        tip_count=Count('beautytip')
    ).order_by('name')
    return render(request, 'admin/tips/categories/list.html', {
        'categories': categories
    })


class AdminTipDeleteView(SuccessMessageMixin, DeleteView):
    model = BeautyTip
    template_name = 'admin/tips/confirm_delete.html'
    success_message = "Beauty tip deleted successfully"
    success_url = reverse_lazy('tips:admin_tip_list')


class AdminTipCategoryCreateView(SuccessMessageMixin, CreateView):
    model = BeautyTipCategory
    fields = ['name', 'description']
    template_name = 'admin/tips/categories/form.html'
    success_message = "Category created successfully"
    success_url = reverse_lazy('tips:admin_tip_category_list')

    def form_valid(self, form):
        if form.instance.name:
            if not form.instance.slug:
                form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)
    

class AdminTipCategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = BeautyTipCategory
    fields = ['name', 'description']
    template_name = 'admin/tips/categories/form.html'
    success_message = "Category updated successfully"
    success_url = reverse_lazy('tips:admin_tip_category_list')

    def form_valid(self, form):
        if form.instance.name:
            if not form.instance.slug:
                form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)
    
class AdminTipCategoryDeleteView(SuccessMessageMixin, DeleteView):
    model = BeautyTipCategory
    template_name = 'admin/tips/categories/confirm_delete.html'
    success_message = "Category deleted successfully"
    success_url = reverse_lazy('tips:admin_tip_category_list')