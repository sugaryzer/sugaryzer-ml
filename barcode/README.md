# Barcode Detection 

This project is a Flask web application that allows you to upload images and detect barcodes using the `pyzbar` library. The app processes the uploaded image to extract and return barcode data (EAN13 and CODE128 types).

## Features
- Run app.py
- Upload an image via a POST request.
- The image is processed using OpenCV to resize and threshold it for better barcode detection.
- Supports EAN13 and CODE128 barcode types.
- Returns the barcode data in the response.

## Requirements

To run this application, you will need the following Python packages:

- Flask
- OpenCV (opencv-python)
- Pyzbar
- NumPy

### Install dependencies

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
