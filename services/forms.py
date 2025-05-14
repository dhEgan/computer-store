from django import forms
from .models import ServiceReview

class ServiceReviewForm(forms.ModelForm):
   class Meta:
        model = ServiceReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(1, '1 Sao'), (2, '2 Sao'), (3, '3 Sao'), (4, '4 Sao'), (5, '5 Sao')]),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Hãy chia sẻ trải nghiệm của bạn về dịch vụ này...'
            }),
        }
    
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'rating-radio'})