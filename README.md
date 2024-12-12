# Model Machine Learning - Sugaryzer

Sugaryzer-ML is an project providing machine learning solutions designed for diverse applications. This repository contains three core ML models:

1. *Analysis Prediction*
2. *Product Recommendation*
3. *OCR (Optical Character Recognition)*

Each model is built to be modular and easily integrable into various pipelines, offering flexibility and scalability for developers and data scientists.

---

## Features

### 1. Product Recommendation Model
This model generates product recommendations based on the similarity of categories owned by the product. This model uses content based filtering with the cosine similarity method.

#### Key Features:
- This model generates product recommendations based on the similarity of categories owned by the product.
- Uses content-based filtering with the cosine similarity method.
  
#### Algorithms Used:
- Content-Based Filtering
- Cosine Similarity

### 2. Analysis Prediction Model
To analyze users' daily consumption, this model uses model-based collaborative filtering using a decission tree. The user's daily consumption will be analyzed per day with the output categorized into 3 different categories namely red, green and yellow.

#### Key Features:
- To analyze users' daily consumption, this model uses model-based collaborative filtering using a decision tree.
- The user's daily consumption is analyzed per day with the output categorized into three categories: red, green, and yellow.

### 3. OCR Model
OCR model that is used to retrieve the product id on the barcode to be linked to the database and used by other models. This model is only a bridge to retrieve the product id.

#### Key Technologies:
- *Deep Learning Frameworks*: TensorFlow, PyZbar
- *Pretrained Models*: fine-tuned CNNs
---

## Project Structure

The repository is organized into the following folders:

- `barcode`: Contains the implementation of the OCR model for barcode scanning.
- `recommender`: Contains the product recommendation model.
- `predict`: Contains the analysis prediction model.
- `data`: Stores datasets required by the models.
- `deploy_flask`: Contains the Flask application for deploying the models as a web service.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sugaryzer/sugaryzer-ml.git
   cd sugaryzer-ml
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the environment:
   - Create a `.env` file based on the provided `.env.example`.
   - Add API keys, model configurations, and other necessary settings.

---

## Usage

### Running the OCR Model:
Navigate to the `barcode` folder and run:
```bash
python run_ocr.py --image_path path/to/image.jpg
```

### Running the Product Recommendation Model:
Navigate to the `recommender` folder and run:
```bash
python run_recommender.py --product_id PRODUCT_ID
```

### Running the Analysis Prediction Model:
Navigate to the `predict` folder and run:
```bash
python run_prediction.py --data_path path/to/data.csv
```

### Deploying with Flask:
Navigate to the `deploy_flask` folder and run:
```bash
python app.py
