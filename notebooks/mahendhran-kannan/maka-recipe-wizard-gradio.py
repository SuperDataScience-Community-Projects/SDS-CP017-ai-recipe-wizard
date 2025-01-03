import time
import gradio as gr
from src.llm_model import LLM_MODELS, llm_init

# Handlers
def generate_recipe(selected_model, user_ingredients):
    """
    This function handles the recipe generation and simulates a live text stream
    by adding a delay between words.
    """
    if not user_ingredients:
        return "Add some ingredients, please!", "", "", ""
    
    # Call the LLM to generate the recipe
    title, ingredients, instructions, image_url = llm_init(selected_model, user_ingredients)
    
    # Streamed response for ingredients and instructions
    ingredients_stream = " ".join(word for word in ingredients.split(" "))
    instructions_stream = " ".join(word for word in instructions.split(" "))
    
    return title, ingredients_stream, instructions_stream, image_url

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🍳 AI Recipe Wizard")
    
    with gr.Row():      
        selected_model = gr.Dropdown(choices=list(LLM_MODELS.keys()), label="Select a LLM Model:")
    
    user_ingredients = gr.Textbox(placeholder="Your magic ingredients for the recipe (e.g., Turmeric, Pepper, Butter)", 
                                  label="Your Ingredients")
    
    generate_button = gr.Button("Click for AI Recipe")
    
    with gr.Row():
        with gr.Column():
            ingredients_box = gr.Textbox(label="Ingredients (Streaming)", lines=10)
            instructions_box = gr.Textbox(label="Instructions (Streaming)", lines=10)
        with gr.Column():
            title_box = gr.Text(label="Recipe Title")
            image_output = gr.Image(label="Dish Image")
    
    # Linking the button to the function
    generate_button.click(
        fn=generate_recipe, 
        inputs=[selected_model, user_ingredients], 
        outputs=[title_box, ingredients_box, instructions_box, image_output]
    )

# Launch the app
#demo.launch()
demo.launch(share=True, server_port=8080)
