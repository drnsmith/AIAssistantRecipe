document.getElementById("recipeForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    // Get user input
    const ingredients = document.getElementById("ingredients").value.split(",");
    const preferences = document.getElementById("preferences").value.split(",");

    // Create payload
    const payload = {
        ingredients: ingredients.map(item => item.trim()),
        preferences: preferences.map(item => item.trim()),
        top_n: 1
    };

    try {
        // Send POST request to the API
        const response = await fetch("http://127.0.0.1:8000/query_recipe", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById("recipeOutput").textContent = JSON.stringify(data, null, 2);
        } else {
            document.getElementById("recipeOutput").textContent = "Error fetching recipe.";
        }
    } catch (error) {
        document.getElementById("recipeOutput").textContent = "An error occurred.";
        console.error("Error:", error);
    }
});
