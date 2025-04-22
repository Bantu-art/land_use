# Land Usage Change Detection System

A Django-based web application for analyzing and detecting changes in land usage patterns by comparing satellite or aerial images over time.

## Project Overview

This system allows users to:
- Upload and compare two images of the same geographical area taken at different times
- Detect and highlight changes in land usage patterns
- Generate reports and visualizations of detected changes
- Track and analyze land usage changes over time

## Features

- **Image Comparison**: Compare two images of the same area taken at different times
- **Change Detection**: Automatically detect and highlight areas where land usage has changed
- **Visualization**: Generate heatmaps and overlays showing the extent of changes
- **Reporting**: Generate detailed reports of detected changes
- **User Management**: Secure user authentication and authorization
- **Data Storage**: Store and manage image data and analysis results

## Technical Stack

- **Backend**: Django 5.2
- **Frontend**: HTML, CSS, JavaScript
- **Image Processing**: OpenCV, NumPy, Matplotlib
- **Database**: SQLite3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Bantu-art/land_use.git
cd land_use
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip3 install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your configuration
# Required settings:
# - SECRET_KEY: Generate a new one using:
#   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
# - DEBUG: Set to True for development, False for production
# - ALLOWED_HOSTS: Add your domain or IP addresses
```

5. Run migrations:
```bash
python3 manage.py migrate
```

6. Create a superuser (optional):
```bash
python3 manage.py createsuperuser
```

7. Start the development server:
```bash
python3 manage.py runserver
```

## Environment Variables

The following environment variables are required:

- `SECRET_KEY`: Django secret key for cryptographic signing
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames
- `MEDIA_ROOT`: Directory for uploaded media files
- `MEDIA_URL`: URL prefix for media files
- `STATIC_ROOT`: Directory for collected static files
- `STATIC_URL`: URL prefix for static files

Optional variables:
- `DATABASE_URL`: Database connection URL (if using SQLite3)
- `EMAIL_*`: Email settings for notifications
- `MAX_IMAGE_SIZE`: Maximum allowed image size in bytes
- `ALLOWED_IMAGE_TYPES`: Comma-separated list of allowed image types

## Project Structure

```
land_use/
├── land_use/          # Project configuration
├── landapp/           # Main application
│   ├── models.py      # Database models
│   ├── views.py       # View logic
│   ├── templates/     # HTML templates
│   └── static/        # Static files
├── manage.py          # Django management script
├── requirements.txt   # Project dependencies
├── .env.example      # Environment variables template
└── .env              # Environment variables (not in version control)
```

## Usage

1. Access the web interface at `http://localhost:8000`
2. Upload two images of the same area taken at different times
3. Configure analysis parameters
4. View the results and generated reports

## Image Requirements

- Supported formats: JPEG, PNG, TIFF
- Recommended resolution: Minimum 1024x1024 pixels
- Images should be of the same geographical area
- Images should be taken from similar angles and lighting conditions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Satellite imagery providers
- Open-source image processing libraries
- Django community

## Contact

For questions or support, please contact the project maintainers.