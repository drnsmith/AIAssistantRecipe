from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import logging

# Initialize the model and tokenizer
def initialize_model(model_name="gpt2"):
    """
    Initialize the GPT model and tokenizer.
    """
    try:
        logging.info(f"Loading model and tokenizer: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        logging.info("Model and tokenizer loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading model or tokenizer: {e}")
        raise RuntimeError("Failed to load model or tokenizer") from e
    
    # Ensure pad_token is set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        logging.info("Tokenizer pad token set to EOS token.")
    
    return tokenizer, model

# Initialize
tokenizer, model = initialize_model()


def generate_recipe_gpt2(context, ingredients=None, preferences=None, max_new_tokens=300):
    """
    Generate a recipe using GPT-2.

    Args:
        context (str): Contextual information (e.g., recipe details or constraints).
        ingredients (str, optional): User-provided ingredients.
        preferences (list, optional): User-provided preferences.
        max_new_tokens (int): Number of new tokens to generate.

    Returns:
        str: Generated recipe from the GPT-2 model.
    """
    logging.info(f"Ingredients: {ingredients}")
    logging.info(f"Preferences: {preferences}")
    logging.info(f"Context: {context}")

    # Construct the user query
    user_query = f"Create a recipe using these ingredients: {ingredients}. Preferences: {preferences}."
    logging.info(f"User Query: {user_query}")

    # Combine user query and context into input text
    input_text = (
        f"Context:\n{context}\n\n"
        f"Please ensure the recipe includes the following ingredients: {ingredients}.\n"
        f"Preferences: {preferences}.\n\n"
        f"Response:"
    )
    logging.info(f"Input Text for Generation: {input_text}")

    # Generate response using the model
    try:
        inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

        outputs = model.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            do_sample=True,
        )
        logging.info("Response generated successfully.")

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logging.info(f"Generated Response: {response}")
        return response.strip()

    except Exception as e:
        logging.error(f"Error during text generation: {e}")
        raise ValueError("Failed to generate recipe.") from e
