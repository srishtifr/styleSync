import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

def build_recommendation_engine(df):
    print("Combining descriptive features...")

    features_to_combine = ['productName', 'colorName', 'colorShades', 'mainCatCode', 'details']
    combined_features = df[features_to_combine].fillna('').agg(' '.join, axis=1)

    print("converting text profiles into math vectors")

    vectorizer = TfidfVectorizer(stop_words='english')
    Tfidf_matrix = vectorizer.fit_transform(combined_features)

    print(f"matrix created with shape : {Tfidf_matrix.shape}")
    return Tfidf_matrix

def get_recommendations(productId, df, Tfidf_matrix, top_n=5):

    try:
        idx = df[df['productId'] == productId].index[0]
    except IndexError:
        print(f"productId '{productId}' not found in the dataset!")
        return None
    
    cosine_sim = cosine_similarity(Tfidf_matrix[idx], Tfidf_matrix).flatten()

    similar_indices = cosine_sim.argsort()[-(top_n + 1):][::-1]

    return df.iloc[similar_indices]

if __name__ == '__main__':
    from preprocess import load_and_clean_data

    DATA_PATH = os.path.join("data", "H&m.csv")
    df = load_and_clean_data(DATA_PATH)

    if df is not None:
        matrix = build_recommendation_engine(df)

        test_id = df['productId'].iloc[0]
        test_name = df['productName'].iloc[0]
        print(f"\nTesting recommendation for:'{test_name}' (ID: {'test_id'})")
        
        recommendations = get_recommendations(test_id, df, matrix, top_n = 5)

    if recommendations is not None:
        print("\nTop 5 recommended items found:")
        print(recommendations[['productId', 'productName', 'colorName', 'price']])



