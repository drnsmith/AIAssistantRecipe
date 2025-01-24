## Agentic Recipe Assistant

### Scenario: Where Data Science Meets AI/ML Engineering
You're part of a team at a cutting-edge culinary tech company, tasked with developing an AI-driven recipe assistant. The goal is transformative: empower users to create and customise recipes based on their unique preferences, available ingredients, and dietary needs—all without endless web searches or scrolling through blogs.

This project represents the perfect intersection of data science and software engineering:

- As a **data scientist**, you leverage cutting-edge models to generate personalised recipes. Using a rich dataset of culinary knowledge, you design algorithms that adapt to user input, refine recipes dynamically, and offer insightful suggestions.
- As a **software engineer**, you build the infrastructure to bring this vision to life. You create APIs, monitor performance, and ensure the system runs efficiently and scalably.

Together, your work enables the assistant to:
- Suggest recipes based on the user’s available ingredients.
- Offer real-time adjustments (e.g., "Make it spicier" or "Add a vegetarian option").
- Provide step-by-step instructions for preparing dishes.
- Learn and adapt to user preferences over time, creating a truly personalised culinary experience.

---

### Overview
The **Agentic Recipe Assistant** is an AI-powered solution designed to transform the way users create and customise recipes. Using technologies like Redis, Prometheus, and FastAPI, the system generates personalised recipes based on user inputs, such as available ingredients, dietary preferences, and cooking styles. The assistant adapts to feedback, refines its suggestions, and learns over time to deliver a seamless user experience.

---

### Features
- **Ingredient-based recipe generation**: Provide a list of ingredients, and the assistant generates tailored recipes.
- **Customisable recipes**: Adjust recipes based on preferences like dietary restrictions or cooking methods.
- **Real-time adaptation**: Modify recipes dynamically (e.g., "Make it spicier" or "Add a vegetarian option").
- **Cache Integration**: Redis caching to optimise performance for frequent queries.
- **Performance Monitoring**: Metrics for API performance and cache usage using Prometheus.
- **Load Testing**: Locust integration to simulate high traffic and monitor scalability.

---
The `data/ folder` is expected to include the following files:

 - `recipe_embeddings.npy` – Precomputed recipe embeddings for similarity-based recommendations.
 - `recipes.csv` – Recipe dataset with titles, ingredients, and directions.

Why is the data missing?
Due to size and licensing constraints, these files are not included. To prepare the data:

1. Obtain an open-source recipe dataset (e.g., Kaggle).
2. Use `app/data_loader.py` to preprocess the dataset.
3. Generate embeddings for recipes using `recipe_logic.py`.
---

### Technologies Used
- **Backend**: FastAPI for API development.
- **Caching**: Redis for optimised performance.
- **Monitoring**: Prometheus for metrics and Grafana for visualisation.
- **Load Testing**: Locust for stress testing.
- **Deployment**: Docker for containerisation and Docker Compose for multi-container orchestration.
- **Data Processing**: NumPy, Pandas for data handling and processing.

---
### Frontend Integration
The frontend/ folder provides a simple user-facing interface. It communicates with the backend APIs to enable real-time interaction.

#### Features
 - Dynamic Input Forms: Input ingredients, preferences, and dietary needs.
 - Interactive Results Display: Recipes are displayed dynamically.
 - API Integration: Calls backend endpoints for live results.

#### Usage
 - Ensure the backend is running:
```bash
uvicorn app.main:app --reload
```
 - Open the `frontend/index.html` file in a browser or serve it locally:
```bash
python -m http.server
```
 - Test features like recipe generation and adjustments.
---

### Installation and Setup

#### Prerequisites
1. **Python 3.8+**
2. **Redis** (Ensure Redis is installed and running locally or in Docker)
3. **Docker** (for containerisation)

#### Clone the Repository
```bash
$ git clone https://github.com/drnsmith/Agentic-Recipe-Assistant.git
$ cd Agentic-Recipe-Assistant
```

#### Backend Setup
1. Create a virtual environment:
   ```bash
   $ python -m venv env
   $ source env/bin/activate   # On Windows: env\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   $ pip install -r requirements.txt
   ```
3. Start Redis (if not already running):
   ```bash
   $ redis-server
   ```
4. Run the backend:
   ```bash
   $ uvicorn app.main:app --reload
   ```

#### Docker Setup
1. Build and run the application using Docker Compose:
   ```bash
   $ docker-compose up --build
   ```

---

### Usage

#### Access the API
1. **Navigate to Swagger UI**
   - Open your browser and go to: `http://localhost:8000/docs`.
   - The Swagger UI provides an interactive way to test all endpoints.

2. **Test the following endpoints:**

   #### **Core Endpoints**
   - **GET /health**  
     Health check to verify the API and Redis connection status.

   - **GET /metrics**  
     Prometheus metrics for monitoring API performance.

   #### **Recipe Endpoints**
   - **POST /recommend**  
     Generate recipe suggestions based on ingredients and preferences.  
     **Body:**
     ```json
     {
       "ingredients": "tomato, onion, garlic",
       "preferences": ["vegetarian"],
       "top_n": 3
     }
     ```
     **Response:** A list of recipe recommendations.

   - **POST /recommend_by_embedding**  
     Generate embedding-based recipe recommendations.  
     **Body:**
     ```json
     {
       "ingredients": "chicken, rice",
       "top_n": 5
     }
     ```
     **Response:** Recipes based on embedding similarity.

   - **POST /generate_ai_recipe**  
     Generate a recipe using AI, based on ingredients and preferences.  
     **Body:**
     ```json
     {
       "ingredients": "chickpeas, spinach",
       "preferences": ["vegan"]
     }
     ```
     **Response:** A customised recipe generated by AI:
     ```json
     {
       "ai_recipe": "Spinach and chickpea curry with coconut milk and Indian spices"
     }
     ```

   - **POST /query_recipe**  
     Retrieve or generate a recipe based on ingredients and preferences, with caching enabled.  
     **Body:**
     ```json
     {
       "ingredients": ["flour", "eggs", "milk"],
       "preferences": ["breakfast"],
       "top_n": 1
     }
     ```
     **Response:** A generated or cached recipe.

   #### **Utility Endpoints**
   - **POST /substitute**  
     Suggest substitutions for a given ingredient.  
     **Body:**
     ```json
     {
       "ingredient": "butter"
     }
     ```
     **Response:** A list of suitable substitutions.

3. Use `http://localhost:8000/metrics` to access Prometheus metrics.

#### Monitor Performance
1. Start Prometheus:
   ```bash
   $ prometheus --config.file=prometheus.yml
   ```
2. Access Prometheus at `http://localhost:9090` to query metrics such as:
   - `cache_hits_total`
   - `cache_misses_total`
   - `api_request_latency_seconds`

#### Load Testing with Locust
1. Run Locust:
   ```bash
   $ locust -f locustfile.py --host=http://localhost:8000
   ```
2. Access Locust at `http://localhost:8089` to simulate user traffic and monitor performance.

---

### Project Structure
```
agentic-recipe-assistant/
├── app/
│   ├── ai_recipe.py           # AI-based recipe generation
│   ├── main.py                # FastAPI application
│   ├── recipe_logic.py        # Recipe recommendation logic
│   ├── ingredient_logic.py    # Ingredient substitution logic
│   ├── data_loader.py         # Dataset loading and pre-processing
│   └── __init__.py
├── data/
│   ├── recipe_embeddings.npy  # Precomputed recipe embeddings
│   ├── recipes.csv            # Recipe dataset
├── frontend/
│   ├── index.html             # Frontend HTML file
│   ├── style.css              # Frontend styles
│   ├── script.js              # Frontend JavaScript logic
├── tests/
│   ├── test_endpoints.py      # API endpoint tests
│   ├── test_integration.py    # Integration tests
│   └── test_utils.py          # Utility tests
|   └── __init__.py
├── requirements.txt           # Python dependencies
├── prometheus.yml             # Prometheus configuration
├── locustfile.py              # Locust load testing script
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Dockerfile for backend
└── README.md                  # Project documentation
```

---

### Roadmap
- [ ] Enhance recipe generation with GPT-based LLMs.
- [ ] Integrate IoT features (e.g., smart fridges).
- [ ] Expand nutritional analysis capabilities.
- [ ] Add multi-user support for collaborative cooking.

---

### Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature-name'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---
## Repository History Cleaned

As part of preparing this repository for collaboration, its commit history has been cleaned. This action ensures a more streamlined project for contributors and removes outdated or redundant information in the history. 

The current state reflects the latest progress as of 24/01/2025.

For questions regarding prior work or additional details, please contact the author.

---

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

