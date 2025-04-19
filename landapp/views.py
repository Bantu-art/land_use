from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import AerialImage

def upload_images(request):
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
