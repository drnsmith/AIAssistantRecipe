from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import logging


def filter_recipes(df, ingredients, preferences):
    """
    Filter recipes based on ingredients and preferences.
    """
    filtered = df.copy()

    # Match ingredients
    if ingredients:
        filtered = filtered[
            filtered['preprocessed_ingredients'].str.contains(ingredients, case=False, na=False)
        ]

    # Match preferences
    if preferences:
        for pref in preferences:
            filtered = filtered[
                filtered['preprocessed_ingredients'].str.contains(pref, case=False, na=False)
            ]

    # Log the filtering process
    logging.info(
        f"Filtered recipes based on ingredients '{ingredients}' and preferences '{preferences}': {filtered.head(5)}"
    )
    return filtered


def recommend_by_embedding(df, embeddings, query_embedding, top_n=3):
    """
    Recommend recipes using preloaded embeddings.
    Args:
        df (DataFrame): The DataFrame containing recipes.
        embeddings (np.ndarray): Preloaded recipe embeddings.
        query_embedding (np.ndarray): Embedding for the query.
        top_n (int): Number of top recommendations to return.
    """
    if embeddings is None or len(embeddings) == 0:
        raise ValueError("Embeddings are missing or empty.")

    if query_embedding is None or len(query_embedding) == 0:
        raise ValueError("Query embedding is missing or empty.")

    # Compute cosine similarities
    similarities = cosine_similarity([query_embedding], embeddings)[0]

    # Get top N results
    top_indices = np.argsort(similarities)[-top_n:][::-1]

    # Log the recommendation process
    logging.info(f"Top {top_n} indices for recommendations: {top_indices}")

    return df.iloc[top_indices]


def create_new_recipe(ingredients, preferences=None):
    """
    Dynamically generate a new recipe.
    Args:
        ingredients (list): List of ingredients for the recipe.
        preferences (list): Optional list of user preferences.
    Returns:
        dict: A dictionary containing the generated recipe.
    """
    if not ingredients or len(ingredients) == 0:
        raise ValueError("Ingredients list cannot be empty.")

    # Construct recipe steps
    steps = [
        f"Step 1: Prepare the ingredients: {', '.join(ingredients)}.",
        "Step 2: Combine the ingredients and cook according to your taste."
    ]

    if preferences:
        steps.append(f"Step 3: Adjust the recipe to match preferences: {', '.join(preferences)}.")

    # Log the recipe generation process
    logging.info(f"Generated a new recipe with ingredients {ingredients} and preferences {preferences}")

    return {
        "title": "Generated Recipe",
        "ingredients": ingredients,
        "preferences": preferences or [],
        "steps": steps
    }
