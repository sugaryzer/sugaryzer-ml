import pandas as pd
import numpy as np
import cv2
import pytesseract
from matplotlib import pyplot as plt

custom_config = r'--oem 3 --psm 6'

img = cv2.imread("img.png", cv2.IMREAD_GRAYSCALE)
# display raw image
plt.imshow(img)
plt.show()

def sharpen_image(im):
  kernel = np.ones((3,3),np.float32)/90
  im = cv2.filter2D(im,-1,kernel)
  return im

img = sharpen_image(img)
# display sharpened image
plt.imshow(img)
plt.show()

img_thresh = cv2.adaptiveThreshold(
    img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
)

# Invert the image
img_thresh = 255 - img_thresh

# Display the thresholded image
plt.imshow(img_thresh, cmap='gray')
plt.axis('off')  # Optional: Hide the axes
plt.show()


def align_text(im):
    coords = np.column_stack(np.where(img_thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    h, w = img.shape
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img_thresh, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


# align image text
img = align_text(img)
# display rotated and aligned image
plt.imshow(img)
plt.show()

kalo