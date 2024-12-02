SCAN BARCODE - PYTESSERACT & EASYOCR

Description:
This is a simple OCR (Optical Character Recognition) API built with Flask, Tesseract, and EasyOCR. The API processes images and extracts text using two different OCR tools: Tesseract and EasyOCR.

Installation:
1. Clone or download the project.
2. Create a Python virtual environment:
   python -m venv venv
3. Activate the virtual environment:
   - On Windows:
     venv\Scripts\activate
   - On macOS/Linux:
     source venv/bin/activate
4. Install dependencies:
   pip install -r requirements.txt
5. Install Tesseract (make sure it's installed and the path is set):
   - Download Tesseract: https://github.com/tesseract-ocr/tesseract
   - Set the path for Tesseract in your script (e.g., in `ocr_script.py`):
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
6. Run the application:
   python app.py
7. Access the API at http://127.0.0.1:5000.

API Endpoints:
- **GET /**: Returns a welcome message with usage instructions.
- **POST /process-image**: Upload an image file for OCR processing. Returns extracted text from the image using both Tesseract and EasyOCR.

Example of using the POST /process-image endpoint with Postman:
1. Open Postman.
2. Set the method to POST (PLEASE PAY ATTENTION!, POST NOT GET).
3. Set the URL to: http://127.0.0.1:5000/process-image
4. In the "Body" tab, choose "form-data" and upload an image under the key "file" (don't forget to upload it first).
5. Send the request to get the OCR results.

Author:
Machine Learning Team
