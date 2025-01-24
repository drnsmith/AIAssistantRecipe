from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.recipe_logic import recommend_by_embedding
from app.data_loader import load_data
from app.ai_recipe import generate_recipe_gpt2
import logging
import redis
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
import pandas as pd
import time


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Backend started")

# Load data and embeddings from files
try:
    recipes_path = "/Users/natashasmith/Desktop/recipe_api/data/updated_recipes_with_generated_embeddings.csv"
    embeddings_path = "/Users/natashasmith/Desktop/recipe_api/data/recipe_embeddings.npy"
    
    df = pd.read_csv(recipes_path)
    embeddings = np.load(embeddings_path)
    
    logging.info("Recipes and embeddings loaded successfully")
except Exception as e:
    logging.error(f"Error loading recipes or embeddings: {e}")
    raise e

# Configure Redis
try:
    redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    redis_client.ping()
    logging.info("Connected to Redis!")
except redis.ConnectionError as e:
    logging.error(f"Redis unavailable: {e}")
    redis_client = None

# Middleware to measure response times
class ResponseTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logging.info(f"{request.method} {request.url} completed in {process_time:.2f} seconds")
        return response

# Initialise FastAPI app
app = FastAPI(
    title="Recipe API",
    description="An API for recommending recipes and generating custom AI recipes.",
    version="1.0.0",
)

# Add middleware for response time tracking
app.add_middleware(ResponseTimeMiddleware)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Recipe API!"}

# Request models
class RecommendRequest(BaseModel):
    ingredients: Optional[str] = None
    preferences: Optional[List[str]] = None
    top_n: int = 3

@app.get("/health")
def health_check():
    redis_status = "connected" if redis_client and redis_client.ping() else "unavailable"
    return {"status": "ok", "redis": redis_status}

# Prometheus metrics
REQUEST_COUNT = Counter("api_requests_total", "Total number of API requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Latency of API requests in seconds", ["endpoint"])

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        endpoint = request.url.path
        method = request.method
        with REQUEST_LATENCY.labels(endpoint=endpoint).time():
            response = await call_next(request)
        http_status = response.status_code
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=http_status).inc()
        return response

app.add_middleware(MetricsMiddleware)

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type="text/plain")

# Recommend recipes using preloaded embeddings
@app.post("/recommend_by_embedding")
def recommend_by_embedding_endpoint(request: RecommendRequest):
    """
    Recommend recipes based on precomputed embeddings.
    """
    logging.info(f"Received request for /recommend_by_embedding: {request}")

    try:
        # Compute cosine similarity
        query_text = f"Ingredients: {request.ingredients or ''}"
        if request.preferences:
            query_text += f"\nPreferences: {', '.join(request.preferences)}"

        # Use precomputed embeddings for similarity
        query_embedding = embeddings.mean(axis=0)  # Example: Placeholder; adjust as needed
        similarities = cosine_similarity([query_embedding], embeddings)[0]
        top_indices = np.argsort(similarities)[-request.top_n:][::-1]

        # Extract recommendations
        results = df.iloc[top_indices][["title", "ingredients", "directions"]].to_dict(orient="records")
        return results
    except Exception as e:
        logging.error(f"Error recommending recipes: {e}")
        raise HTTPException(status_code=500, detail="Error generating recommendations")

@app.post("/generate_ai_recipe")
def generate_ai_recipe(request: RecommendRequest):
    """
    Generate a new recipe using AI and embeddings-based context.
    """
    logging.info(f"Received request for /generate_ai_recipe: {request}")

    try:
        # Filter recipes using embeddings
        query_embedding = embeddings.mean(axis=0)  # Placeholder: Replace with query-specific embedding logic
        similarities = cosine_similarity([query_embedding], embeddings)[0]
        top_indices = np.argsort(similarities)[-request.top_n:][::-1]

        # Construct context from top matching recipes
        similar_recipes = df.iloc[top_indices][["title", "ingredients", "directions"]].to_dict(orient="records")
        context = " ".join([f"{recipe['title']}: {recipe['directions']}" for recipe in similar_recipes])

        # Generate new recipe using GPT-2
        ai_generated_recipe = generate_recipe_gpt2(
            context=context,
            ingredients=request.ingredients,
            preferences=request.preferences
        )
        return {"ai_recipe": ai_generated_recipe}
    except Exception as e:
        logging.error(f"Error generating AI recipe: {e}")
        raise HTTPException(status_code=500, detail="Error generating AI recipe")

@app.post("/query_recipe")
def query_recipe(request: RecommendRequest):
    """
    Query recipes using precomputed embeddings.
    """
    try:
        # Filter recipes based on embeddings
        query_embedding = embeddings.mean(axis=0)  # Example: Placeholder; adjust as needed
        similarities = cosine_similarity([query_embedding], embeddings)[0]
        top_indices = np.argsort(similarities)[-request.top_n:][::-1]
        results = df.iloc[top_indices][["title", "ingredients", "directions"]].to_dict(orient="records")
        return results
    except Exception as e:
        logging.error(f"Error querying recipe: {e}")
        raise HTTPException(status_code=500, detail="Error querying recipe")
