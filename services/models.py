from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models import Avg
from django.utils.text import slugify



    


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = 'Service Category'
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()
    image = models.ImageField(upload_to='services/', blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    average_rating = models.FloatField(default=0.0)
    review_count = models.PositiveIntegerField(default=0)

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            self.review_count = reviews.count()
        else:
            self.average_rating = 0.0
            self.review_count = 0
        self.save(update_fields=['average_rating', 'review_count'])

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})

    def duration_in_minutes(self):
        return self.duration.total_seconds() // 60
    
    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.name)  
        super().save(*args, **kwargs)
    

class ServiceReview(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service Review'
        verbose_name_plural = 'Service Reviews'
        unique_together = ('service', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s review for {self.service.name}"

    def get_rating_stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)