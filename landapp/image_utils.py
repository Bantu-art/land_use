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

def classify_changes(img1, img2, change_mask):
    # Convert to HSV for better color analysis
    hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    
    # Create output image
    output = img2.copy()
    
    # Find contours of changes
    contours, _ = cv2.findContours(change_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Process each changed region
    for contour in contours:
        if cv2.contourArea(contour) < 100:  # Ignore small changes
            continue
            
        # Get the bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        
        # Extract the region from both images
        region1 = hsv1[y:y+h, x:x+w]
        region2 = hsv2[y:y+h, x:x+w]
        
        # Calculate average color in the region
        avg1 = np.mean(region1, axis=(0,1))
        avg2 = np.mean(region2, axis=(0,1))
        
        # Determine type of change based on color differences
        hue_diff = abs(avg1[0] - avg2[0])
        sat_diff = abs(avg1[1] - avg2[1])
        val_diff = abs(avg1[2] - avg2[2])
        
        # Color code different types of changes
        if val_diff > 30:  # Significant brightness change
            color = (0, 255, 255)  # Yellow for major changes
        elif hue_diff > 20:  # Color change
            color = (0, 165, 255)  # Orange for color changes
        else:
            color = (0, 255, 0)  # Green for subtle changes
            
        # Draw the contour
        cv2.drawContours(output, [contour], -1, color, 2)
        
    return output

def process_images(img1_path, img2_path):
    # Read images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    # Resize images to match
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    
    # Detect changes
    change_mask = detect_land_changes(img1, img2)
    
    # Classify and visualize changes
    result = classify_changes(img1, img2, change_mask)
    
    # Convert BGR to RGB for matplotlib
    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    plt.imshow(result_rgb)
    plt.title('Land Use Change Detection')
    
    # Create legend
    legend_elements = [
        Patch(facecolor='yellow', edgecolor='yellow', label='Major Changes'),
        Patch(facecolor='orange', edgecolor='orange', label='Color Changes'),
        Patch(facecolor='green', edgecolor='green', label='Subtle Changes')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.axis('off')
    plt.tight_layout()
    
    # Save plot to BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    # Convert to base64 string
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return image_base64 