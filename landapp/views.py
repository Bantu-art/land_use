from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import AerialImage
from .image_utils import process_images
import os
from django.conf import settings

def upload_images(request):
    """
    Handle the upload of two images via a form.

    If the request method is POST, validate the forms and save the uploaded images.
    If both forms are valid, redirect to the 'compare' view with the IDs of the uploaded images.
    If the request method is GET, render the upload form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered upload page or a redirect to the 'compare' view.
    """
    if request.method == 'POST':
        form1 = ImageUploadForm(request.POST, request.FILES, prefix="img1")
        form2 = ImageUploadForm(request.POST, request.FILES, prefix="img2")
        if form1.is_valid() and form2.is_valid():
            img1 = form1.save()
            img2 = form2.save()
            return redirect('compare', img1_id=img1.id, img2_id=img2.id)
    else:
        form1 = ImageUploadForm(prefix="img1")
        form2 = ImageUploadForm(prefix="img2")
    return render(request, 'upload.html', {'form1': form1, 'form2': form2})

def compare_images(request, img1_id, img2_id):
    """
    Compare two uploaded images and display the result.

    Retrieve the images by their IDs, process them, and render the comparison result.

    Args:
        request (HttpRequest): The HTTP request object.
        img1_id (int): The ID of the first image.
        img2_id (int): The ID of the second image.

    Returns:
        HttpResponse: The rendered comparison page with the images and the result.
    """
    img1 = AerialImage.objects.get(id=img1_id)
    img2 = AerialImage.objects.get(id=img2_id)
    
    # Get absolute paths of the images
    img1_path = os.path.join(settings.MEDIA_ROOT, str(img1.image))
    img2_path = os.path.join(settings.MEDIA_ROOT, str(img2.image))
    
    # Process the images
    result_image = process_images(img1_path, img2_path)
    
    context = {
        'img1': img1,
        'img2': img2,
        'result_image': result_image
    }
    
    return render(request, 'compare.html', context)
