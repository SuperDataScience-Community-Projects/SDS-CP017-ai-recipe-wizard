import json
from mdutils.mdutils import MdUtils
from openai import OpenAI  
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


def convert_to_md(dishInstructions, recipeImageURL):
    # Initialize MdUtils without a file name
    mdFile = MdUtils(file_name='', title='Enjoy the recipe')

    jsonvalue = parse_json_markdown(dishInstructions)

    print(jsonvalue['dishName'])
    print(''.join(jsonvalue['ingredients']))
    print(jsonvalue['cookingInstructions'])

    mdFile.new_header(level=1, title=f"{jsonvalue['dishName']}")
    mdFile.new_header(level=2, title='Ingredients')
    mdFile.new_list(jsonvalue['ingredients'])
    mdFile.new_header(level=2, title='Cooking instructions')
    mdFile.new_paragraph(jsonvalue['cookingInstructions'])
    
    if recipeImageURL != "":
        mdFile.new_header(level=2, title='Image')
        mdFile.new_paragraph(f"'![Dish]({recipeImageURL})'")

    # Get the markdown text
    recipe_markdown = mdFile.get_md_text()

    # Print the markdown text (or use it as needed)
    return recipe_markdown


def parse_json_markdown(json_string: str) -> dict:
    # Remove the triple backticks if present
    json_string = json_string.strip()
    start_index = json_string.find("```json")
    end_index = json_string.find("```", start_index + len("```json"))

    if start_index != -1 and end_index != -1:
        extracted_content = json_string[start_index + len("```json"):end_index].strip()
        
        # Parse the JSON string into a Python dictionary
        parsed = json.loads(extracted_content)
    elif start_index != -1 and end_index == -1 and json_string.endswith("``"):
        end_index = json_string.find("``", start_index + len("```json"))
        extracted_content = json_string[start_index + len("```json"):end_index].strip()
        
        # Parse the JSON string into a Python dictionary
        parsed = json.loads(extracted_content)
    elif json_string.startswith("{"):
        # Parse the JSON string into a Python dictionary
        parsed = json.loads(json_string)
    else:
        raise Exception("Could not find JSON block in the output.")

    return parsed


def get_chat_llm(model_name, api_key):

    if model_name.startswith("gpt-"):
        return ChatOpenAI(model_name=model_name, openai_api_key=api_key, streaming=True)
    elif model_name.startswith("gemini-"):
        return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key, streaming=True)
    else:
        raise ValueError(f"Unsupported model: {model_name}")

def get_image_llm(model_name, api_key):
    # if model_name.startswith("gpt-"):
    #     image_model = OpenAI(api_key=api_key)
    #     return image_model

    image_model = OpenAI(api_key=api_key)
    return image_model
    
