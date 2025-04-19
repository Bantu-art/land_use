from django import forms
from .models import AerialImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = AerialImage
        fields = ['title', 'image']
