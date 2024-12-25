from transformers import pipeline
import streamlit as st

# Load the pre-trained model pipeline (using a Hugging Face hosted model)
generator = pipeline("text-generation", model="tiiuae/falcon-7b-instruct", tokenizer="tiiuae/falcon-7b-instruct")

def generate_recipe(ingredients):
    # Prompt engineering
    prompt = f"""
    You are a world-class chef. Based on the following ingredients, create a unique recipe:
    Ingredients: {ingredients}.
    Provide:
    1. A title for the recipe.
    2. A list of ingredients (with quantities).
    3. Step-by-step instructions to prepare the dish.
    """
    
    # Generate recipe
    response = generator(prompt, max_length=300, temperature=0.8, num_return_sequences=1)
    return response[0]["generated_text"]

# Streamlit app setup
st.title("AI Recipe Wizard 🍳")
st.subheader("Generate creative recipes based on your ingredients!")

# Input ingredients
ingredients = st.text_area("Enter your ingredients (comma-separated):", "tomato, chicken, garlic")

# Generate recipe
if st.button("Generate Recipe"):
    with st.spinner("Cooking up your recipe..."):
        recipe = generate_recipe(ingredients)
    st.success("Here is your recipe:")
    st.text(recipe)

# Footer
st.write("Built with 💖 using Generative AI!")
