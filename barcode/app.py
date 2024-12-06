import os
import cv2
from flask import Flask, request, jsonify
from pyzbar.pyzbar import decode, ZBarSymbol

app = Flask(__name__)


# Fungsi untuk membaca barcode dari gambar
def read_barcode(image_path):
    try:
        # Membaca gambar dalam mode grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Resize dan aplikasikan thresholding
        img = cv2.resize(img, (300, 300))
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Decode barcode
        decoded_objects = decode(img, symbols=[ZBarSymbol.EAN13, ZBarSymbol.CODE128])

        # Mengembalikan data barcode pertama yang ditemukan
        if decoded_objects:
            barcode = decoded_objects[0].data.decode('utf-8')
            return barcode

        return None
    except Exception as e:
        return str(e)


# Cek dan buat folder uploads jika belum ada
if not os.path.exists('uploads'):
    os.makedirs('uploads')


# API route untuk mendeteksi barcode dari gambar yang diunggah
@app.route('/detect_barcode', methods=['POST'])
def detect_barcode():
    try:
        # Periksa apakah file ada dalam request
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        # Pastikan file yang diunggah adalah gambar yang valid
        if file:
            # Tentukan path untuk menyimpan gambar yang diunggah
            image_path = os.path.join('uploads', file.filename)

            # Simpan file gambar sementara
            file.save(image_path)

            # Panggil fungsi deteksi barcode
            barcode = read_barcode(image_path)

            if barcode:
                return jsonify({"barcode": barcode}), 200
            else:
                return jsonify({"error": "No barcode detected"}), 404
        else:
            return jsonify({"error": "Invalid file type"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Jalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True)
