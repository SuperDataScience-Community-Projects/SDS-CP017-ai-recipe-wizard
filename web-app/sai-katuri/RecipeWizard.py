import gradio as gr
from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
from phi.tools.dalle import Dalle
from phi.model.openai import OpenAIChat
from dotenv import load_dotenv
from phi.utils.pprint import pprint_run_response
from IPython.display import Image, display
from typing import Iterator

# Load environment variables
load_dotenv()

# Custom CSS for styling
custom_css = """
#title {
    text-align: center;
    color: #ff5733;  /* Example color (bright orange) */
    font-size: 36px;
    font-weight: bold;
}
"""


# Define the agents
Recipe_Generator_agent = Agent(
    name="Recipe Generator",
    role="Generate a recipe",
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=[
        "Always include recipe name, ingredients, Cuisine, Time to cook, and instructions in the response. "
        "Include any modifications to the recipe to make it vegan or gluten-free or allergen-free. "
        "Include any links for the recipe by searching the web. Also generate a recipe"
        "create a summary of the recipe useful for creating images of the recipe."
    ],
    show_tool_calls=True,
    markdown=True,
    description="Generate a recipe.",
)

extract_ImageSummary_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    name="Summary Extractor",
    role="Extract summary from the response",
    instructions=["Extract summary from the response to create image of the recipe."],
    show_tool_calls=True,
    markdown=True,
    description="Extract image summary.",
)

image_generator_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[Dalle()],
    description="You are an AI agent that can generate images using DALL-E.",
    instructions="When the user asks you to create an image, use the `create_image` tool to create the image.",
    markdown=True,
    num_images=1,
    show_tool_calls=True,
)

# Gradio app logic
def generate_recipe_and_image(prompt):
    # Step 1: Generate the recipe
    recipe_response: Iterator[RunResponse] = Recipe_Generator_agent.run(prompt)
    recipe_text = recipe_response.content 
    
    # Step 2: Extract the image summary
    summary_response: Iterator[RunResponse] = extract_ImageSummary_agent.run(recipe_text)
    image_summary = summary_response.content  

    # Step 3: Generate the image
    image_generator_agent.print_response(image_summary, stream=True)
    images = image_generator_agent.get_images()

    # Return recipe text and image URL
    if images and isinstance(images, list):
        for image_response in images:
            image_url = image_response.url
    return recipe_text,image_url

# Gradio interface
def app():
    with gr.Blocks() as demo:
        gr.Markdown('# Recipe Generator with AI')
        with gr.Row():
            prompt = gr.Textbox(label="Enter your recipe prompt", lines=2, placeholder="E.g., Spaghetti with vegan sauce")
        with gr.Row():
            generate_button = gr.Button("Generate Recipe and Image")
        with gr.Row():
            recipe_output = gr.Markdown(label="Generated Recipe")
            image_output = gr.Image(label="Generated Image")

        # Define the interaction
        generate_button.click(fn=generate_recipe_and_image, inputs=[prompt], outputs=[recipe_output, image_output])
    return demo

# Run the app
if __name__ == "__main__":
    app().launch()
