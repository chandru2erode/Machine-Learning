#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys
# Importing sys (system specific parameters and functions) library
import cv2
# Importing the Opencv Library
import numpy as np
# Importing NumPy,which is the fundamental package for scientific computing with Python
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
# Importing Pytesseract, which is an OCR engine for Character Recognition computing with Python

# Reading Image
img = cv2.imread(sys.argv[1])
cv2.namedWindow("Original Image",cv2.WINDOW_NORMAL)
# Creating a Named window to display image
cv2.imshow("Original Image",img)
# Display image
cv2.waitKey(0)

"""
#print img.shape

# Image Resizing
r = 100.0 / img.shape[1]
dim = (100, int(img.shape[0] * r))
 
# perform the actual resizing of the image and show it
resized_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
cv2.namedWindow("Resized Image",cv2.WINDOW_NORMAL)
# Creating a Named window to display image
cv2.imshow("resized", resized_img)
# Display resized image
cv2.waitKey(0)
"""

# Cropping image to 60% of bottom area
cropped_img = img[(img.shape[0])//2:img.shape[0]]
cv2.namedWindow("Cropped Bottom Image",cv2.WINDOW_NORMAL)
# Creating a Named window to display image
cv2.imshow("Cropped Bottom Image",img)
# Display Image
cv2.waitKey(0)

# RGB to Gray scale conversion
img_gray = cv2.cvtColor(cropped_img,cv2.COLOR_RGB2GRAY)
cv2.namedWindow("Gray Converted Image",cv2.WINDOW_NORMAL)
# Creating a Named window to display image
cv2.imshow("Gray Converted Image",img_gray)
# Display Image
cv2.waitKey(0)

# Noise removal with iterative bilateral filter(removes noise while preserving edges)
noise_removal = cv2.bilateralFilter(img_gray,9,75,75)
cv2.namedWindow("Noise Removed Image",cv2.WINDOW_NORMAL)
# Creating a Named window to display image
cv2.imshow("Noise Removed Image",noise_removal)
# Display Image
cv2.waitKey(0)

# Histogram equalisation for better results
equal_histogram = cv2.equalizeHist(noise_removal)
cv2.namedWindow("After Histogram equalisation",cv2.WINDOW_NORMAL)
# Creating a Named window to display image
cv2.imshow("After Histogram equalisation",equal_histogram)
# Display Image
cv2.waitKey(0)

# Morphological opening with a rectangular structure element
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
morph_image = cv2.morphologyEx(equal_histogram,cv2.MORPH_OPEN,kernel,iterations=15)
cv2.namedWindow("Morphological opening",cv2.WINDOW_NORMAL)
# Creating a Named window to display image
cv2.imshow("Morphological opening",morph_image)
# Display Image
cv2.waitKey(0)

# Image subtraction(Subtracting the Morphed image from the histogram equalised Image)
sub_morp_image = cv2.subtract(equal_histogram,morph_image)
cv2.namedWindow("Subtraction image", cv2.WINDOW_NORMAL)
# Creating a Named window to display image
cv2.imshow("Subtraction image", sub_morp_image)
# Display Image
cv2.waitKey(0)

# Thresholding the image
ret,thresh_image = cv2.threshold(sub_morp_image,0,255,cv2.THRESH_OTSU)
cv2.namedWindow("Image after Thresholding",cv2.WINDOW_NORMAL)
# Creating a Named window to display image
cv2.imshow("Image after Thresholding",thresh_image)
# Display Image
cv2.waitKey(0)

# Applying Canny Edge detection
canny_image = cv2.Canny(thresh_image,250,255)
cv2.namedWindow("Image after applying Canny",cv2.WINDOW_NORMAL)
# Creating a Named window to display image
cv2.imshow("Image after applying Canny",canny_image)
# Display Image
canny_image = cv2.convertScaleAbs(canny_image)
cv2.waitKey(0)

# dilation to strengthen the edges
kernel = np.ones((3,3), np.uint8)
# Creating the kernel for dilation
dilated_image = cv2.dilate(canny_image,kernel,iterations=1)
cv2.namedWindow("Dilation", cv2.WINDOW_NORMAL)
# Creating a Named window to display image
cv2.imshow("Dilation", dilated_image)
# Displaying Image
cv2.waitKey(0)

# Finding Contours in the image based on edges
new,contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours= sorted(contours, key = cv2.contourArea, reverse = True)[:10]
# Sort the contours based on area ,so that the number plate will be in top 10 contours
screenCnt = None
# loop over our contours
for c in contours:
 # approximate the contour
 peri = cv2.arcLength(c, True)
 approx = cv2.approxPolyDP(c, 0.06 * peri, True)  # Approximating with 6% error
 # if our approximated contour has four points, then
 # we can assume that we have found our screen
 if len(approx) == 4:  # Select the contour with 4 corners
  screenCnt = approx
  break
final = cv2.drawContours(cropped_img, [screenCnt], -1, (0, 255, 0), 3)
# Drawing the selected contour on the original image
cv2.namedWindow("Image with Selected Contour",cv2.WINDOW_NORMAL)
# Creating a Named window to display image
cv2.imshow("Image with Selected Contour",final)
cv2.waitKey(0)

# Masking the part other than the number plate
mask = np.zeros(img_gray.shape,np.uint8)
new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
new_image = cv2.bitwise_and(cropped_img,cropped_img,mask=mask)
cv2.namedWindow("Final_image",cv2.WINDOW_NORMAL)
cv2.imshow("Final_image",new_image)
cv2.waitKey(0)

# Histogram equal for enhancing the number plate for further processing
y,cr,cb = cv2.split(cv2.cvtColor(new_image,cv2.COLOR_RGB2YCrCb))
# Converting the image to YCrCb model and splitting the 3 channels
y = cv2.equalizeHist(y)
# Applying histogram equalisation
final_image = cv2.cvtColor(cv2.merge([y,cr,cb]),cv2.COLOR_YCrCb2RGB)
# Merging the 3 channels
cv2.namedWindow("Enhanced Number Plate",cv2.WINDOW_NORMAL)
# Creating a Named window to display image
cv2.imshow("Enhanced Number Plate",final_image)
# Display image
cv2.imwrite("Output_img.jpg",final_image)
cv2.waitKey() # Wait for a keystroke from the user

#print(pytesseract.image_to_boxes(final_image))
# print(pytesseract.image_to_string(Image.open('Output_img.jpg')))
f = open('Output_file.txt','wb') 
# Creating a file for Output storage 
f.write(pytesseract.image_to_string(final_image))
# Converting image to text and writing it in the file 
f.close() 
# Closing the file
