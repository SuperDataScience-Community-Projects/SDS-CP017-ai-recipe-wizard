from src.utils import extract_section
from src.prompt_setup import prompt_setup

# Function to send a prompt to generate recipe
def generate_text(client, _model, input):
  
        prompt = prompt_setup(input)
        response = client.chat.completions.create(
            model=_model,  
            messages=[
                {"role": "system", "content": "You are a world-renowned chef"},
                {"role": "user", "content":prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
           
        )

   
        # Extract recipe content
        recipe_content = response.choices[0].message.content
        
        # Extract the sections
        #title, ingredients, instructions, summary = extract_section(recipe_content)
        title = extract_section(recipe_content, "Title") 
        ingredients = extract_section(recipe_content, "Ingredients")
        instructions = extract_section(recipe_content, "Instructions")
        summary = extract_section(recipe_content, "Summary")

        
        return title, ingredients, instructions, summary   