from django.db import models

class AerialImage(models.Model):
    """
    Represents an aerial image uploaded by the user.

    Attributes:
        title (str): The title or name of the image.
        image (ImageField): The uploaded image file, stored in the 'uploads/' directory.
        uploaded_at (DateTimeField): The timestamp when the image was uploaded.
    """
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
