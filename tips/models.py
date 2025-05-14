from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class BeautyTipCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Beauty Tip Categories"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BeautyTip(models.Model):
    category = models.ForeignKey(BeautyTipCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='tips/', blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while BeautyTip.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if not self.slug:  
            return reverse('tips:admin_tip_list')
        return reverse('tips:detail', kwargs={'slug': self.slug})

    def excerpt(self, length=100):
        return self.content[:length] + '...' if len(self.content) > length else self.content
    
    def increment_views(self):
        
        self.views = models.F('views') + 1
        self.save(update_fields=['views'])