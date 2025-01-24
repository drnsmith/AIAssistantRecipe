import os
import pandas as pd
import numpy as np
import ast

def load_data():
    # Load recipe dataset
    csv_path = "data/updated_recipes_with_generated_embeddings.csv"
    df = pd.read_csv(csv_path)

    # Convert ingredients column to lists
    if 'ingredients' in df.columns:
        df['ingredients'] = df['ingredients'].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        )

    # Load precomputed embeddings
    npy_path = "data/recipe_embeddings.npy"
    embeddings = np.load(npy_path)

    return df, embeddings
