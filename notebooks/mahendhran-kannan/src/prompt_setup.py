def prompt_setup(user_ingredients):
    prompt = f"""
    Please generate a recipe based on the following ingredients or given description: {user_ingredients}.
    Structure your response in the following format:

    Title: <Recipe Title>

    Ingredients:
    - <Ingredient 1>
    - <Ingredient 2>
    - ...

    Instructions:
    1. <Step 1>
    2. <Step 2>
    3. ...

    Summary: Provide a 1-2 sentence summary describing the appearance and presentation of the finished dish, suitable for visual representation (e.g., "A golden brown apple crisp with a crumbly cinnamon topping, garnished with fresh apple slices and a dollop of whipped cream.").
    """
    return prompt