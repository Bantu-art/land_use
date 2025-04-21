"""
Image processing utilities for land use change detection.

This module provides functions for detecting and visualizing changes between two aerial images.
It uses OpenCV for image processing and matplotlib for visualization.
"""

import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for Django
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from io import BytesIO
import base64

def detect_land_changes(img1, img2, threshold=30):
    """
    Detect changes between two aerial images using LAB color space analysis.
    
    This function converts images to LAB color space for better change detection,
    computes differences in each channel, and applies thresholding and morphological
    operations to clean up the result.
    
    Args:
        img1 (numpy.ndarray): First input image in BGR format
        img2 (numpy.ndarray): Second input image in BGR format
        threshold (int, optional): Threshold value for binary conversion. Defaults to 30.
        
    Returns:
        numpy.ndarray: Binary mask indicating changed regions (255 for changes, 0 for no change)
    """
    # Convert images to LAB color space for better change detection
    lab1 = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)
    lab2 = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)
    
    # Split into channels
    l1, a1, b1 = cv2.split(lab1)
    l2, a2, b2 = cv2.split(lab2)
    
    # Compute differences in each channel
    diff_l = cv2.absdiff(l1, l2)
    diff_a = cv2.absdiff(a1, a2)
    diff_b = cv2.absdiff(b1, b2)
    
    # Combine differences
    combined_diff = cv2.addWeighted(diff_l, 0.5, diff_a, 0.25, 0)
    combined_diff = cv2.addWeighted(combined_diff, 1, diff_b, 0.25, 0)
    
    # Apply threshold
    _, thresh = cv2.threshold(combined_diff, threshold, 255, cv2.THRESH_BINARY)
    
    # Apply morphological operations to clean up the result
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    return thresh

# ... existing code ...