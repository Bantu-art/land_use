from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from landapp.models import AerialImage
import os
from django.conf import settings
from PIL import Image
from io import BytesIO

class ViewsTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        # Create a test image using PIL
        image = Image.new('RGB', (100, 100), color='red')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )
        self.upload_url = reverse('upload')
        self.compare_url = reverse('compare', args=[1, 2])  # Will be updated in tests

    def test_upload_page_get(self):
        """Test that the upload page loads correctly."""
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload.html')
        self.assertIn('form1', response.context)
        self.assertIn('form2', response.context)

    def test_upload_images_success(self):
        """Test successful image upload."""
        # Create new test images
        image1 = Image.new('RGB', (100, 100), color='red')
        image2 = Image.new('RGB', (100, 100), color='blue')
        
        image1_io = BytesIO()
        image2_io = BytesIO()
        
        image1.save(image1_io, format='JPEG')
        image2.save(image2_io, format='JPEG')
        
        img1 = SimpleUploadedFile(
            name='test_image1.jpg',
            content=image1_io.getvalue(),
            content_type='image/jpeg'
        )
        img2 = SimpleUploadedFile(
            name='test_image2.jpg',
            content=image2_io.getvalue(),
            content_type='image/jpeg'
        )
        
        data = {
            'img1-title': 'Image 1',
            'img1-image': img1,
            'img2-title': 'Image 2',
            'img2-image': img2,
        }
        response = self.client.post(self.upload_url, data)
        
        # Debug information
        if response.status_code != 302:
            print("Response content:", response.content.decode())
            if 'form1' in response.context:
                print("Form1 errors:", response.context['form1'].errors)
            if 'form2' in response.context:
                print("Form2 errors:", response.context['form2'].errors)
        
        # Check that we were redirected
        self.assertEqual(response.status_code, 302)
        
        # Check that the images were created
        self.assertEqual(AerialImage.objects.count(), 2)
        
        # Get the created images
        img1 = AerialImage.objects.get(title='Image 1')
        img2 = AerialImage.objects.get(title='Image 2')
        
        # Check that we were redirected to the compare page
        self.assertRedirects(
            response,
            reverse('compare', args=[img1.id, img2.id])
        )

    def test_upload_images_invalid(self):
        """Test upload with invalid data."""
        # Create a test image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )
        
        data = {
            'img1-title': '',  # Invalid: empty title
            'img1-image': test_image,
            'img2-title': 'Image 2',
            'img2-image': test_image,
        }
        response = self.client.post(self.upload_url, data)
        
        # Check that we stayed on the same page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload.html')
        
        # Check that no images were created
        self.assertEqual(AerialImage.objects.count(), 0)

    def test_compare_page(self):
        """Test the compare page."""
        # Create a test image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )
        
        # Create two images first
        img1 = AerialImage.objects.create(
            title='Image 1',
            image=test_image
        )
        
        # Create another test image for img2
        image_io.seek(0)
        test_image2 = SimpleUploadedFile(
            name='test_image2.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )
        
        img2 = AerialImage.objects.create(
            title='Image 2',
            image=test_image2
        )
        
        # Create actual image files
        img1_path = os.path.join(settings.MEDIA_ROOT, str(img1.image))
        img2_path = os.path.join(settings.MEDIA_ROOT, str(img2.image))
        os.makedirs(os.path.dirname(img1_path), exist_ok=True)
        os.makedirs(os.path.dirname(img2_path), exist_ok=True)
        
        # Save the actual image files
        image.save(img1_path, format='JPEG')
        image.save(img2_path, format='JPEG')
        
        response = self.client.get(
            reverse('compare', args=[img1.id, img2.id])
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compare.html')
        self.assertIn('img1', response.context)
        self.assertIn('img2', response.context)
        self.assertIn('result_image', response.context)

    def test_compare_page_nonexistent_images(self):
        """Test compare page with nonexistent image IDs."""
        response = self.client.get(
            reverse('compare', args=[999, 1000])
        )
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        """Clean up test files."""
        # Clean up any test files that were created
        for image in AerialImage.objects.all():
            if image.image:
                if os.path.isfile(image.image.path):
                    os.remove(image.image.path) 