from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('predict_consume.h5')

app = Flask(__name__)

@app.route('/')
def home():
    return "Sugar Consumption Prediction API"

@app.route('/predict', methods=['POST'])
def predict():
    try:

        data = request.get_json()
        daily_sugar_intake = data.get('daily_sugar_intake', None)

        if daily_sugar_intake is None:
            return jsonify({"error": "Please provide daily_sugar_intake parameter."}), 400

        if not isinstance(daily_sugar_intake, (int, float)):
            return jsonify({"error": "daily_sugar_intake must be a number."}), 400

        input_data = np.array([[daily_sugar_intake]])
        prediction = model.predict(input_data)

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


if __name__ == '__main__':
    app.run(debug=True)
