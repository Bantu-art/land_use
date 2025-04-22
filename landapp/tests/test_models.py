from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from landapp.models import AerialImage
import os
from django.conf import settings

class AerialImageModelTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # Empty content for testing
            content_type='image/jpeg'
        )

    def test_create_aerial_image(self):
        """Test creating a new aerial image."""
        image = AerialImage.objects.create(
            title='Test Image',
            image=self.test_image
        )
        self.assertEqual(image.title, 'Test Image')
        self.assertTrue(image.uploaded_at is not None)
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, image.image.name)))

    def test_title_max_length(self):
        """Test that title cannot exceed max_length."""
        long_title = 'a' * 101  # 101 characters
        image = AerialImage(title=long_title, image=self.test_image)
        with self.assertRaises(ValidationError):
            image.full_clean()

    def test_title_required(self):
        """Test that title is required."""
        image = AerialImage(image=self.test_image)
        with self.assertRaises(ValidationError):
            image.full_clean()

    def test_image_required(self):
        """Test that image is required."""
        image = AerialImage(title='Test Image')
        with self.assertRaises(ValidationError):
            image.full_clean()

    def test_string_representation(self):
        """Test the string representation of the model."""
        image = AerialImage.objects.create(
            title='Test Image',
            image=self.test_image
        )
        self.assertEqual(str(image), 'Test Image')

    def tearDown(self):
        """Clean up test files."""
        # Clean up any test files that were created
        for image in AerialImage.objects.all():
            if image.image:
                if os.path.isfile(image.image.path):
                    os.remove(image.image.path) 