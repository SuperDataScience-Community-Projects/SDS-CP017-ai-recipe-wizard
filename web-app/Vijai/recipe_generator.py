import openai
import json
from __init__ import client  # Import the client object from __init__.py

def generate_full_output_with_template(user_input):
    """
    Generate a structured recipe, image prompt, ingredient suggestions, and nutritional information in one prompt.

    Args:
        user_input (dict): A dictionary containing:
            - ingredients (str): A comma-separated list of ingredients.
            - dietary_restrictions (str): Dietary restrictions (e.g., vegetarian, vegan, gluten-free).
            - cuisine_preferences (str): Preferred cuisine type.
            - time_constraints (str): Time constraints for the meal.

    Returns:
        dict: A structured dictionary containing:
            - recipe_details (dict): Title, ingredients, and instructions.
            - image_prompt (str): A concise image generation prompt.
            - ingredient_suggestions (list): Suggested additional ingredients.
            - nutrition_info (dict): Nutritional breakdown.
    """
    # Extract user inputs
    ingredients = user_input.get("ingredients", "none")
    dietary_restrictions = user_input.get("dietary_restrictions", "none")
    cuisine_preferences = user_input.get("cuisine_preferences", "none")
    time_constraints = user_input.get("time_constraints", "none")

    # Prepare the prompt with a clear template
    messages = [
        {"role": "system",
         "content": "You are an expert chef, food photographer, and nutritionist. Always respond in the JSON template provided below."},
        {"role": "user",
         "content": f"Create a recipe using the following ingredients: {ingredients}. "
                    f"Take into account these preferences: "
                    f"Dietary restrictions: {dietary_restrictions}, "
                    f"Cuisine preferences: {cuisine_preferences}, "
                    f"Time constraints: {time_constraints}. "
                    f"Respond in the following JSON format:\n\n"
                    f"{{\n"
                    f"  \"recipe_details\": {{\n"
                    f"    \"title\": \"<Recipe Title>\",\n"
                    f"    \"ingredients\": [\"<Ingredient 1>\", \"<Ingredient 2>\", ...],\n"
                    f"    \"instructions\": [\"<Step 1>\", \"<Step 2>\", ...]\n"
                    f"  }},\n"
                    f"  \"image_prompt\": \"<A concise description of the dish>\",\n"
                    f"  \"ingredient_suggestions\": [\"<Suggestion 1>\", \"<Suggestion 2>\", ...],\n"
                    f"  \"nutrition_info\": {{\n"
                    f"    \"calories\": \"<Calories>\",\n"
                    f"    \"protein\": \"<Protein>\",\n"
                    f"    \"carbohydrates\": \"<Carbohydrates>\",\n"
                    f"    \"fats\": \"<Fats>\"\n"
                    f"  }}\n"
                    f"}}"}
    ]

    try:
        # Call GPT-4 API
        response = client.chat.completions.create(
            model="gpt-4",
            #model= "llama3.2",
            messages=messages,
            max_tokens=1500,
            temperature=0.7
        )

        # Extract raw content
        raw_content = response.choices[0].message.content

        # Debug: Print raw content
        print("Raw GPT Response:", raw_content)

        # Parse the JSON response
        structured_response = json.loads(raw_content)

        # Extract fields from structured response
        recipe_details = structured_response.get("recipe_details", {})
        image_prompt = structured_response.get("image_prompt", "Not provided")
        ingredient_suggestions = structured_response.get("ingredient_suggestions", [])
        nutrition_info = structured_response.get("nutrition_info", {})

        return {
            "recipe_details": recipe_details,
            "image_prompt": image_prompt,
            "ingredient_suggestions": ingredient_suggestions,
            "nutrition_info": nutrition_info
        }

    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        print(f"Error parsing JSON response: {e}")
        print("Raw GPT Response (invalid JSON):", raw_content)
        return {
            "recipe_details": "Failed to parse recipe details.",
            "image_prompt": "Failed to parse image prompt.",
            "ingredient_suggestions": [],
            "nutrition_info": {}
        }
    except openai.OpenAIError as e:
        # Handle OpenAI API errors
        print(f"Error generating full output: {e}")
        return {
            "recipe_details": "Failed to generate recipe details.",
            "image_prompt": "Failed to generate image prompt.",
            "ingredient_suggestions": [],
            "nutrition_info": {}
        }