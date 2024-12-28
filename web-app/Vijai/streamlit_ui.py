import streamlit as st
import base64
import os
import matplotlib.pyplot as plt
from io import BytesIO
from recipe_generator import generate_full_output_with_template
from image_creator import generate_image
from piechart import create_nutrition_pie_chart
import re


# Function to extract numerical values from the dictionary
def extract_numerical_values(nutrition_dict):
    numerical_values = {}
    for key, value in nutrition_dict.items():
        # Use regex to extract the numerical part
        numerical_values[key] = int(re.search(r'\d+', value).group())
    return numerical_values

# Function to set the background image
def set_background_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to convert a local image to a base64-encoded URL
def get_local_image_url(file_path):
    with open(file_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded}"

# Function to create a pie chart for nutrition info
def create_nutrition_pie_chart(nutrition_info):
    labels = list(nutrition_info.keys())
    values = list(nutrition_info.values())

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title("Nutritional Breakdown")

    # Convert plot to image
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf

def run_app():
    # Set the background image
    current_dir = os.path.dirname(__file__)  # Get the directory of the current script
    background_path = os.path.join(current_dir, "background.jpeg")
    set_background_image(get_local_image_url(background_path))

    # App title
    st.title("Smart Recipe Generator 🍽️")
    st.write("Generate creative recipes and their visualizations with AI!")

    # User input for ingredients
    ingredients = st.text_area("Enter ingredients (comma-separated):", placeholder="e.g., chicken, rice, garlic")

    # Additional user inputs
    dietary_restrictions = st.selectbox(
        "Select dietary restrictions:",
        options=["none", "vegetarian", "vegan", "gluten-free"],
        index=0  # Default to "none"
    )
    cuisine_preferences = st.selectbox(
        "Select cuisine preferences:",
        options=["none", "Italian", "Indian", "Mexican", "Chinese", "Mediterranean"],
        index=0  # Default to "none"
    )
    time_constraints = st.selectbox(
        "Select time constraints:",
        options=["none", "quick meals under 30 minutes", "elaborate meals (60+ minutes)"],
        index=0  # Default to "none"
    )

    # Generate Recipe and Image button
    if st.button("Generate Recipe and Image"):
        # Validate input
        if not ingredients.strip():
            st.error("Please enter ingredients to generate a recipe.")
            return

        # Call recipe generation function
        with st.spinner("Generating recipe..."):
            try:
                # Combine all user inputs into a single input for recipe generation
                full_input = {
                    "ingredients": ingredients,
                    "dietary_restrictions": dietary_restrictions,
                    "cuisine_preferences": cuisine_preferences,
                    "time_constraints": time_constraints,
                }
                output = generate_full_output_with_template(full_input)

                # Extract results from the response
                recipe_details = output.get("recipe_details", {})
                image_prompt = output.get("image_prompt", "Not provided")
                ingredient_suggestions = output.get("ingredient_suggestions", [])
                nutrition_info = output.get("nutrition_info", {})

                st.success("Recipe generated successfully!")
            except Exception as e:
                st.error(f"Error generating recipe: {e}")
                return

        # Display recipe details
        # Display recipe details
        st.subheader("Generated Recipe")

        # 1. Display title in heading font with underline
        recipe_title = recipe_details.get('title', 'Not provided')
        st.markdown(f"### **{recipe_title}**")
        st.markdown("<hr style='border:1px solid black;'>", unsafe_allow_html=True)

        # 2. Display ingredients as a bullet-point list
        st.markdown("#### Ingredients:")
        ingredients = recipe_details.get("ingredients", [])
        if ingredients:
            for ingredient in ingredients:
                st.markdown(f"- {ingredient}")
        else:
            st.markdown("No ingredients provided.")

        # 3. Display instructions as a numbered list
        st.markdown("#### Instructions:")
        instructions = recipe_details.get("instructions", [])
        if instructions:
            for idx, instruction in enumerate(instructions, 1):
                st.markdown(f"{idx}. {instruction}")
        else:
            st.markdown("No instructions provided.")

        # Display additional ingredient suggestions
        st.subheader("Ingredient Suggestions")
        st.text("\n".join(ingredient_suggestions))

        # Display nutrition information
        st.subheader("Nutrition Information")
        st.json(nutrition_info)
        nutrition_info = extract_numerical_values(nutrition_info)
        nutrition_info.pop('calories', None)  # Remove 'calories' if it exists
        print(nutrition_info)

        # Generate and display pie chart for macronutrient contribution
        if nutrition_info:
            st.subheader("Macronutrient Contribution to Calories")
            try:
                nutrition_chart = create_nutrition_pie_chart(nutrition_info)
                if nutrition_chart:
                    st.image(nutrition_chart, caption="Macronutrient Breakdown")
            except ValueError as e:
                st.error(f"Error generating macronutrient pie chart: {e}")

        # Generate image from the prompt
        with st.spinner("Generating image..."):
            try:
                image_url = generate_image(image_prompt)
                st.success("Image generated successfully!")
            except Exception as e:
                st.error(f"Error generating image: {e}")
                return

        # Display the image
        st.subheader("Generated Dish Image")
        st.image(image_url, caption="Dish Visualization", use_container_width=True)

if __name__ == "__main__":
    run_app()