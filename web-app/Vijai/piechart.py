import matplotlib.pyplot as plt
from io import BytesIO
import streamlit as st

def create_nutrition_pie_chart(nutrition_info):
    """
    Create a pie chart showing how macronutrients contribute to total grams.

    Args:
        nutrition_info (dict): Nutritional information with keys like 'protein',
        'carbohydrates', and 'fats'.

    Returns:
        BytesIO: A buffer containing the pie chart image.
    """
    try:
        # Debugging output using st.write
        st.write("Nutrition Info Inside Function:", nutrition_info)

        # Extract numeric values
        protein = int(nutrition_info.get("protein", 0))
        carbohydrates = int(nutrition_info.get("carbohydrates", 0))
        fats = int(nutrition_info.get("fats", 0))

        st.write(f"Parsed Values -> Protein: {protein}, Carbs: {carbohydrates}, Fats: {fats}")

        # Prepare data for the pie chart
        labels = ['Protein', 'Carbohydrates', 'Fats']
        values = [protein, carbohydrates, fats]

        # Custom function to display grams instead of percentages
        def grams_autopct(pct):
            total = sum(values)
            value = int(round(pct * total / 100.0))  # Convert percentage to actual value
            return f"{value}g"

        # Generate pie chart
        fig, ax = plt.subplots()
        ax.pie(
            values,
            labels=labels,
            autopct=grams_autopct,  # Use the custom function here
            startangle=140,
            colors=['#4CAF50', '#FFC107', '#2196F3']
        )
        ax.set_title("Macronutrient Contribution to Total Grams")

        # Convert plot to image
        buf = BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)  # Close the figure to avoid memory issues
        return buf

    except Exception as e:
        st.error(f"Error Parsing Nutrition Info: {nutrition_info}")
        raise ValueError(f"Invalid nutrition data: {e}")