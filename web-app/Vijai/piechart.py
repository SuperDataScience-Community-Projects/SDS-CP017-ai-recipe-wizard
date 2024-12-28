import matplotlib.pyplot as plt
from io import BytesIO

import matplotlib.pyplot as plt
from io import BytesIO

def create_nutrition_pie_chart(nutrition_info):
    """
    Create a pie chart showing how macronutrients contribute to total calories.

    Args:
        nutrition_info (dict): Nutritional information with keys like 'protein',
        'carbohydrates', and 'fats'.

    Returns:
        BytesIO: A buffer containing the pie chart image.
    """
    try:
        print("Nutrition Info Inside Function:", nutrition_info)  # Debugging

        # Extract numeric values
        protein = int(nutrition_info.get("protein", 0))
        carbohydrates = int(nutrition_info.get("carbohydrates", 0))
        fats = int(nutrition_info.get("fats", 0))

        print(f"Parsed Values -> Protein: {protein}, Carbs: {carbohydrates}, Fats: {fats}")  # Debugging

        # Calculate calorie contributions
        protein_calories = protein * 4  # 1g protein = 4 calories
        carb_calories = carbohydrates * 4  # 1g carb = 4 calories
        fat_calories = fats * 9  # 1g fat = 9 calories

        # Prepare data for the pie chart
        labels = ['Protein', 'Carbohydrates', 'Fats']
        values = [protein_calories, carb_calories, fat_calories]

        # Generate pie chart
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#4CAF50', '#FFC107', '#2196F3'])
        ax.set_title("Macronutrient Contribution to Total Calories")

        # Convert plot to image
        buf = BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)  # Close the figure to avoid memory issues
        return buf

    except Exception as e:
        print(f"Error Parsing Nutrition Info: {nutrition_info}")  # Debugging
        raise ValueError(f"Invalid nutrition data: {e}")
