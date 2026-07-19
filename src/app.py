from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from preprocess import load_and_clean_data
from models import build_recommendation_engine, get_recommendations

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))

# Global variables to store our data and ML matrix in memory
df = None
tfidf_matrix = None

def initialize_backend():
    global df, tfidf_matrix
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(PROJECT_ROOT, "data", "h&m.csv")
    
    print("--- [Flask Boot] Loading fashion dataset... ---")
    df = load_and_clean_data(DATA_PATH)
    if df is not None:
        print("--- [Flask Boot] Building vector similarity matrix... ---")
        tfidf_matrix = build_recommendation_engine(df)
        print("--- [Flask Boot] Success! StyleSync Engine is Live. ---")

# 1. Route to serve your HTML page
@app.route('/')
def home():
    return render_template('index.html')

# 2. API Route to get all products (for our search dropdown list)
@app.route('/api/products', methods=['GET'])
def get_products():
    if df is None:
        return jsonify({"error": "Dataset not loaded"}), 500
    
    # Grab unique products to populate our dropdown
    products_sample = df[['productId', 'productName', 'colorName']].drop_duplicates().head(200)
    list_of_products = products_sample.to_dict(orient='records')
    return jsonify(list_of_products)

# 3. API Route to calculate and return recommendations
# 3. API Route to calculate and return recommendations
@app.route('/api/recommend', methods=['GET'])
def recommend():
    product_id = request.args.get('id')
    if not product_id:
        return jsonify({"error": "Missing product ID parameter"}), 400
        
    # --- ADD THIS LINE TO FIX THE DATA TYPE MATCHING ---
    try:
        product_id = int(product_id)
    except ValueError:
        pass # Keep as string if it contains letters, but standard numeric IDs will be correctly converted
    # ---------------------------------------------------
        
    if df is None or tfidf_matrix is None:
        return jsonify({"error": "Engine not initialized"}), 500

    # Run our Phase 2 matching machine learning model
    recommendations = get_recommendations(product_id, df, tfidf_matrix, top_n=4)
    
    if recommendations is not None:
        result = recommendations[['productId', 'productName', 'brandName', 'colorName', 'price', 'details']].to_dict(orient='records')
        print("Recommendations:")
        print(recommendations)
        print(type(recommendations))    
        return jsonify(result)
    else:
        return jsonify({"error": "Product not found or processing failed"}), 404

if __name__ == '__main__':
    initialize_backend()
    # Run the server locally on port 5000
    app.run(debug=True, port=5000)