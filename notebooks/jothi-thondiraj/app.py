from huggingface_hub import InferenceClient
from PIL import Image
import gradio as gr
import os
import json
# Function to generate recipe from ingredients
def generate_recipe(ingredients: str, model_name_recipe: str, token: str) -> str:
    """
    Generates a recipe based on input ingredients using an LLM.
    Args:
        ingredients (str): Ingredients input by the user.
        model_name_recipe (str): Hugging Face model for text generation.
        token (str): API token for Hugging Face authentication.
    Returns:
        str: Generated recipe text.
    """
    prompt = f"Generate a recipe using the following ingredients: {ingredients}. Write the recipe in detail along with a suitable title."
    client = InferenceClient(model_name_recipe, token=token)
    try:
        response = client.post(
            json={
                "inputs": prompt,
                "parameters": {"max_new_tokens": 500},
                "task": "text-generation",
            }
        )
        return json.loads(response.decode())[0]["generated_text"]
    except Exception as e:
        return f"Error generating recipe: {e}"    
# Function to generate image of the recipe
def generate_image(recipe_title: str, model_name_image: str, token: str) -> Image.Image:
    """
    Generates an image based on the recipe title using a text-to-image model.
    Args:
        recipe_title (str): Title of the recipe to use as the prompt.
        model_name_image (str): Hugging Face model for image generation.
        token (str): API token for Hugging Face authentication.
    Returns:
        PIL.Image.Image: Generated image.
    """
    client = InferenceClient(model_name_image, token=token)
    try:
        prompt = f"A photo the dish: {recipe_title}, showing delicious presentation."
        return client.text_to_image(prompt)
    except Exception as e:
        print(f"Error generating image: {e}")
        return None    
# Gradio function that combines both recipe generation and image generation
def generate_recipe_and_image(message: str, history):
    token = os.getenv("API_Token_HF_AIrecipe")  # Ensure your Hugging Face token is set in environment variables
    model_name_recipe = "microsoft/Phi-3-mini-4k-instruct"  # Replace with the LLM model of your choice
    model_name_image = "prompthero/openjourney"  # Replace with the image generation model of your choice
    
    # Generate recipe
    recipe_text = generate_recipe(message, model_name_recipe, token)
    prompt_to_remove = f"Generate a recipe using the following ingredients: {message}. Write the recipe in detail along with a suitable title."
    if prompt_to_remove in recipe_text:
        recipe_text = recipe_text.replace(prompt_to_remove, "").strip()
    # print("recipe_text:",recipe_text)
    # Extract recipe title from generated recipe text
    lines = recipe_text.split("\n")
    for line in lines:
        if line.lower().startswith("title:"):  # Case-insensitive match
            recipe_title = line.replace("Title:", "").strip()  # Extract and clean title
            break 
    print("recipe_title",recipe_title)    
    # Generate image for the recipe
    recipe_image = generate_image(recipe_title, model_name_image, token)
    image_path = "./recipe_image.png"
    recipe_image.save(image_path, format="PNG")
    
    # Combine text and image
    return recipe_text, gr.Image(value=image_path)    
    

if __name__ == "__main__":
    # Gradio UI
    with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
        gr_image = gr.Image(render=False)
        with gr.Row():
            with gr.Column(scale=4):
                gr.Markdown("<center><h1>AI Recipe Chatbot</h1></center>")
                chatbot = gr.ChatInterface(
                    generate_recipe_and_image,
                    examples=["chicken, rice, tomatoes, onions, spices", "oats, milk, fruits", "Noodles, Tofu, Soy sauce"],
                    type="messages",
                    additional_outputs=[gr_image]
                )
            with gr.Column(scale=1):
                gr.Markdown("<center><h1>Recipe Image</h1></center>")
                # recipe_image = gr.Image(label="Generated Recipe Image")
                gr_image.render()  
    demo.launch()






