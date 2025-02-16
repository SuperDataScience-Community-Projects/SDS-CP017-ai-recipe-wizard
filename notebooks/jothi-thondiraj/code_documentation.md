
# Code Documentation for AI Recipe Chatbot
This documentation is for the app.py file. This is the main file to use. The primary goal of this Python script is to generate a recipe based on the provided ingredients using open source LLMs such as Falcon-7B and integrate it with image generation models like stable diffusion to produce an image of the recipe. 
## Purpose
The purpose of this documentation is to ensure developers can understand, maintain, and extend the AI Recipe Chatbot application efficiently.

---

## Main Components

### 1. `generate_recipe`
Generates a detailed recipe using ingredients provided by the user.

- **Arguments:**
  - `ingredients` (str): List of ingredients.
  - `model_name_recipe` (str): Hugging Face text generation model.
  - `token` (str): Hugging Face API token.

- **Returns:** A string containing the generated recipe.

### 2. `generate_image`
Generates an image of the recipe based on its title.

- **Arguments:**
  - `recipe_title` (str): Title of the recipe.
  - `model_name_image` (str): Hugging Face text-to-image model.
  - `token` (str): Hugging Face API token.

- **Returns:** A PIL image object.

### 3. `generate_recipe_and_image`
Combines recipe generation and image creation into a single Gradio interface.

- **Arguments:**
  - `message` (str): User's input message.
  - `history`: Chat history (Gradio specific).

- **Returns:** Generated recipe text and an image rendered in Gradio.

---

## Key Models Used
- Text Generation: `microsoft/Phi-3-mini-4k-instruct`
- Image Generation: `prompthero/openjourney`

---

## Environment Variables
- `API_Token_HF_AIrecipe`: Hugging Face API token required for authentication.

---

## Development Tools
- **Gradio:** For building the user interface.
- **Hugging Face Hub:** For accessing pre-trained models.

---
