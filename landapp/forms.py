from django import forms
from .models import AerialImage

class ImageUploadForm(forms.ModelForm):
    """
    A form for uploading aerial images.

    This form is based on the AerialImage model and allows users to upload an image
    along with a title.

    Meta:
        model (AerialImage): The model associated with this form.
        fields (list): The fields to include in the form ('title' and 'image').
    """
    class Meta:
        model = AerialImage
        fields = ['title', 'image']
