# Sugaryzer Deploy

This project is a Flask-based API that provides three main functionalities:
1. Barcode detection from uploaded images.
2. Product recommendations based on category and low sugar intake.
3. Daily sugar intake prediction category with health advice.

## Features

### 1. Barcode Detection
Uploads an image to extract and read barcodes (EAN-13 or CODE128).

### 2. Product Recommendations
Recommends low-sugar products in the same category based on a product ID.

### 3. Prediction
Predicts daily sugar intake categories (`hijau`, `kuning`, `merah`) and provides health advice.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Virtual environment (optional)
- Required libraries:
  - Flask
  - TensorFlow
  - pandas
  - scikit-learn
  - NumPy
  - OpenCV
  - pyzbar

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/low-sugar-recommender.git
2. Navigate to the project directory:
   ```bash
   cd deploy_flask
3. Create and activate a virtual environment (optional):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
5. Place the required models and dataset in the root directory:
   - low_sugar_recommender_model.h5
   - predict_consume.h5
   - products_fixed.csv
6. Run the application:
   ```bash
   python app.py
7. Access the API at http://127.0.0.1:5000.


