from pydantic import BaseModel, validator, root_validator
from typing import List, Optional

class RecommendRequest(BaseModel):
    """
    Model for recipe recommendation requests.
    """
    ingredients: Optional[str] = None
    preferences: Optional[List[str]] = None
    top_n: int = 3

    @validator("top_n")
    def validate_top_n(cls, value):
        """
        Ensure top_n is a positive integer.
        """
        if value <= 0:
            raise ValueError("top_n must be a positive integer.")
        return value

    @root_validator
    def validate_request(cls, values):
        """
        Ensure at least one of ingredients or preferences is provided.
        """
        ingredients = values.get("ingredients")
        preferences = values.get("preferences")

        if not ingredients and not preferences:
            raise ValueError("At least one of 'ingredients' or 'preferences' must be provided.")
        return values


class GenerateAIRecipeRequest(BaseModel):
    """
    Model for AI-generated recipe requests.
    """
    ingredients: str
    preferences: Optional[List[str]] = None

    @validator("ingredients")
    def validate_ingredients(cls, value):
        """
        Ensure ingredients are provided and non-empty.
        """
        if not value.strip():
            raise ValueError("Ingredients must be a non-empty string.")
        return value


class RecipeResponse(BaseModel):
    """
    Model for recipe response.
    """
    title: str
    ingredients: List[str]
    preferences: Optional[List[str]] = None
    steps: List[str]


