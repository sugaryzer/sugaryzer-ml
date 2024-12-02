import pytesseract
import easyocr
import numpy as np
import cv2
from PIL import Image

def preprocess_barcode_image(image):
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((1, 3), np.uint8)
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=1)
    return Image.fromarray(dilated)

def clean_barcode_text(text):
    numbers_only = ''.join(filter(str.isdigit, text))
    return numbers_only

def tesseract_read(image):
    processed_image = preprocess_barcode_image(image)
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(processed_image, config=custom_config)
    return clean_barcode_text(text)

def easyocr_read(image):
    reader = easyocr.Reader(['en'], gpu=False)  # Disable GPU for simplicity
    processed_image = preprocess_barcode_image(image)
    img_array = np.array(processed_image)
    results = reader.readtext(img_array)
    text_results = [x[-2] for x in results]
    return clean_barcode_text(" ".join(text_results))
