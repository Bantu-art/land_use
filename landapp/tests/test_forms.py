from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from landapp.forms import ImageUploadForm
from landapp.models import AerialImage
from PIL import Image
from io import BytesIO
import os

class ImageUploadFormTest(TestCase):
    def setUp(self):
        """Set up test data."""
        # Create a test image using PIL
        image = Image.new('RGB', (100, 100), color='red')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )

    def test_valid_form(self):
        """Test form with valid data."""
        form_data = {
            'title': 'Test Image',
        }
        form_files = {
            'image': self.test_image
        }
        form = ImageUploadForm(form_data, form_files)
        if not form.is_valid():
            print("Form errors:", form.errors)  # Debug information
        self.assertTrue(form.is_valid())

    def test_form_without_title(self):
        """Test form without title."""
        form_data = {}
        form_files = {
            'image': self.test_image
        }
        form = ImageUploadForm(form_data, form_files)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_without_image(self):
        """Test form without image."""
        form_data = {
            'title': 'Test Image',
        }
        form = ImageUploadForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)

    def test_form_with_long_title(self):
        """Test form with title exceeding max_length."""
        form_data = {
            'title': 'a' * 101,  # 101 characters
        }
        form_files = {
            'image': self.test_image
        }
        form = ImageUploadForm(form_data, form_files)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_save(self):
        """Test form save method."""
        # Create a new test image since the previous one was consumed
        image = Image.new('RGB', (100, 100), color='red')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )
        
        form_data = {
            'title': 'Test Image',
        }
        form_files = {
            'image': test_image
        }
        form = ImageUploadForm(form_data, form_files)
        if not form.is_valid():
            print("Form errors:", form.errors)  # Debug information
        self.assertTrue(form.is_valid())
        image = form.save()
        self.assertEqual(image.title, 'Test Image')
        self.assertTrue(image.image.name.endswith('test_image.jpg'))

    def tearDown(self):
        """Clean up test files."""
        # Clean up any test files that were created
        for image in AerialImage.objects.all():
            if image.image:
                if os.path.isfile(image.image.path):
                    os.remove(image.image.path) 