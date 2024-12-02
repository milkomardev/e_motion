from django import forms
from e_motion.common.models import GalleryImage


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
        }
