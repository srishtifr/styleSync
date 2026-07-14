import pandas as pd
import os
def load_and_clean_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: COuld not find the dataset at the given path.")
        return None
    
    print("loading fashion dataset...")

    df=pd.read_csv(file_path)
    print(f"Dataset successfully loaded! Found {df.shape[0]} products and {df.shape[1]} columns.")

    print("\n Columns in your dataset:")
    print(df.columns.to_list())

    text_columns = df.select_dtypes(include=['object']).columns
    df[text_columns] = df[text_columns].fillna('unknown')

    print('\nData cleaning completed!')
    return df

if __name__ == "__main__":
    DATA_PATH = os.path.join("data", "H&m.csv")

    cleaned_df = load_and_clean_data(DATA_PATH)
    if cleaned_df is not None:
        print("\nDataset Preview:")
        print(cleaned_df.head())