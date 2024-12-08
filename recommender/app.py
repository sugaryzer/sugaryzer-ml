from flask import Flask, request, jsonify
import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

app = Flask(__name__)

model = tf.keras.models.load_model('low_sugar_recommender_model.h5', custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
data = pd.read_csv("products_fixed.csv")

scaler = MinMaxScaler()
data['sugar_intake'] = data['sugar_intake'].str.replace(',', '.').astype(float)
data = data.dropna()
data['normalized_sugar_intake'] = scaler.fit_transform(data[['sugar_intake']])


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


@app.route('/recommend', methods=['GET'])
def recommend():
    product_id = request.args.get('product_id', type=int)
    
    if product_id is None:
        return jsonify({"error": "Product ID is required."}), 400

    recommendations = recommend_based_on_product_id(product_id)

    return jsonify(recommendations)


if __name__ == "__main__":
    app.run(debug=True)
