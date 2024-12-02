from flask import Flask, request, jsonify
from ocr_script import tesseract_read, easyocr_read
from PIL import Image, UnidentifiedImageError
import io
import logging
import pytesseract
# Inisialisasi Flask
app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Konfigurasi Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Endpoint Root
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the OCR API!",
        "usage": "Send a POST request to /process-image with an image file."
    })


# Endpoint untuk Proses Gambar
@app.route('/process-image', methods=['POST'])
def process_image():
    # Check if the file is present in the request
    if 'file' not in request.files:
        logger.error("No file part in the request")
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        logger.error("No file selected for upload")
        return jsonify({"error": "No selected file"}), 400

    try:
        img_data = file.read()
        image = Image.open(io.BytesIO(img_data))
        image.verify()

        image_format = image.format
        app.logger.info(f"Image format: {image_format}")

        if image_format not in ['JPEG', 'PNG']:
            logger.error(f"Unsupported image format: {image_format}")
            return jsonify({"error": "Unsupported image format"}), 400

        # Reopen the image
        image = Image.open(io.BytesIO(img_data))

        # Run OCR using Tesseract and EasyOCR
        logger.info("Processing image with Tesseract and EasyOCR...")
        tesseract_result = tesseract_read(image)
        easyocr_result = easyocr_read(image)

        # Return OCR results
        return jsonify({
            "tesseract_result": tesseract_result,
            "easyocr_result": easyocr_result
        })

    except UnidentifiedImageError:
        logger.error("Uploaded file is not a valid image")
        return jsonify({"error": "Invalid image file"}), 400

    except Exception as e:
        logger.exception("An error occurred during processing")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
