from flask import Flask, request, jsonify
import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import os
import cv2
from pyzbar.pyzbar import decode, ZBarSymbol

app = Flask(__name__)

# Load the recommendation model
recommender_model = tf.keras.models.load_model('low_sugar_recommender_model.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
data = pd.read_csv("products_fixed.csv")

# Normalize sugar intake
scaler = MinMaxScaler()
data['sugar_intake'] = data['sugar_intake'].str.replace(',', '.').astype(float)
data = data.dropna()
data['normalized_sugar_intake'] = scaler.fit_transform(data[['sugar_intake']])

# Recommender utility
def create_category_embeddings(categories):
    vocabulary = sorted(list(set(categories)))
    cat_to_idx = {cat: idx for idx, cat in enumerate(vocabulary)}
    num_categories = len(vocabulary)
    one_hot = np.zeros((len(categories), num_categories))
    for i, cat in enumerate(categories):
        one_hot[i, cat_to_idx[cat]] = 1
    return one_hot

categories = create_category_embeddings(data['category'])

def recommend_based_on_product_id(product_id, sugar_threshold=20, n=5):
    if product_id not in data['product_id'].values:
        return f"Error: Product ID '{product_id}' not found in the dataset."

    product_info = data[data['product_id'] == product_id].iloc[0]
    category = product_info['category']

    recommended_products = data[
        (data['category'] == category) &
        (data['sugar_intake'] < sugar_threshold) &
        (data['product_id'] != product_id)
        ].sort_values(by='sugar_intake', ascending=True).head(n)

    if recommended_products.empty:
        return f"No low-sugar products found in the same category."

    return recommended_products[['product_id', 'product_name', 'category', 'sugar_intake']].to_dict(orient="records")

# Barcode utility
def read_barcode(image_path):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (300, 300))
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        decoded_objects = decode(img, symbols=[ZBarSymbol.EAN13, ZBarSymbol.CODE128])

        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')
        return None
    except Exception as e:
        return str(e)

# Ensure uploads folder exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Load the consumption prediction model
predict_model = tf.keras.models.load_model('predict_consume.h5')

@app.route('/deploy/barcode', methods=['POST'])
def detect_barcode():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file:
            image_path = os.path.join('uploads', file.filename)
            file.save(image_path)
            barcode = read_barcode(image_path)
            if barcode:
                return jsonify({"barcode": barcode}), 200
            return jsonify({"error": "No barcode detected"}), 404
        return jsonify({"error": "Invalid file type"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/deploy/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        product_id = data.get('product_id', None)
        if product_id is None:
            return jsonify({"error": "Product ID is required."}), 400

        recommendations = recommend_based_on_product_id(product_id)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/deploy/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        daily_sugar_intake = data.get('daily_sugar_intake', None)

        if daily_sugar_intake is None:
            return jsonify({"error": "Please provide daily_sugar_intake parameter."}), 400

        if not isinstance(daily_sugar_intake, (int, float)):
            return jsonify({"error": "daily_sugar_intake must be a number."}), 400

        input_data = np.array([[daily_sugar_intake]])
        prediction = predict_model.predict(input_data)

        categories = ["hijau", "kuning", "merah"]
        predicted_category = categories[np.argmax(prediction)]

        advice = {
            "kuning": "Konsumsi gula harian di bawah normal.",
            "hijau": "Konsumsi gula harian normal.",
            "merah": "Konsumsi gula harian berlebihan."
        }

        return jsonify({
            "advice": advice[predicted_category],
            "category": predicted_category,
            "total": daily_sugar_intake
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)