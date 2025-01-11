
from typing import List
from pydantic import BaseModel
from pydantic import Field

from langchain.chains import LLMChain
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai import OpenAI
import gradio as gr

from src.helper import parse_json_markdown
from src.helper import convert_to_md
from src.helper import get_chat_llm
from src.helper import get_image_llm

import os


SYSTEM_PROMPT='You are an extemely talented and top Chef with expertise in every type of cuisine and can make delicious food.Generate receipe a dinner receipe with name, ingredients and step by step instructions.'

class Recipe(BaseModel):
    dishName: str = Field(description="Recipe Name")
    ingredients: List[str] = Field(description="All ingredients for the recipe")
    cookingInstructions: str = Field(description="Step by Step instructions on how to cook the dish")


def getRecipeImage(recipeDetails):


    image_params = {
        "model": "dall-e-3",  
        "n": 1,               
        "size": "1024x1024",  
        "prompt": f'Authentic dish image of {recipeDetails}',     
        }
    

    try:
        response_image = image_llm.images.generate(**image_params)
        return response_image.data[0].url
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""

def getRecipe(user_prompt, history):

    recipe_out_parser = PydanticOutputParser(pydantic_object=Recipe)
    history_langchain_format = []
    # history_langchain_format.append(SystemMessage(SYSTEM_PROMPT))
    history_langchain_format.append(('system', SYSTEM_PROMPT))


    for msg in history:
        if msg['role'] == "user":
            history_langchain_format.append(('human', msg['content']))
        elif msg['role'] == "assistant":
            history_langchain_format.append(('ai', msg['content']))

    history_langchain_format.append(('human', user_prompt))
    history_langchain_format.append(("human", "Here is your recipe \n{format_instructions}\n{query}"))

    recipe_prompt = ChatPromptTemplate.from_messages(history_langchain_format)
    recipe_prompt.input_variables=["query"]
    recipe_prompt.output_parser = recipe_out_parser
    recipe_prompt.partial_variables = {"format_instructions": recipe_out_parser.get_format_instructions()}
    model = ChatOpenAI( model="gpt-4o-mini")
    llm_chain = LLMChain(llm=model, prompt=recipe_prompt)
    outputRecipe = llm_chain.run("Give me receipe")

    recipe_json = parse_json_markdown(outputRecipe)

    print(f"THIS IS THE DISH : {recipe_json['dishName']}") 
    print(f"ITS INGREDIENTS : {''.join(recipe_json['ingredients'])}")


    recipeImageURL = getRecipeImage(recipe_json['dishName'])
    
    print (f"Image URL: {recipeImageURL}")

    return convert_to_md(outputRecipe, recipeImageURL)

def predict(message, history):
    history_langchain_format = []
    history_langchain_format.append(SystemMessage(SYSTEM_PROMPT))
    for msg in history:
        if msg['role'] == "user":
            history_langchain_format.append(HumanMessage(content=msg['content']))
        elif msg['role'] == "assistant":
            history_langchain_format.append(AIMessage(content=msg['content']))
    history_langchain_format.append(HumanMessage(content=message))
    llm_response = getRecipe(message, history)
    return llm_response

def startWizard(chat_model, image_model):

    # print(f"OPEN AI KEY : {os.environ['OPENAI_API_KEY']}")

    global chat_llm 
    global image_llm

    chat_llm = get_chat_llm(chat_model)
    image_llm = get_image_llm(image_model)

    demo = gr.ChatInterface(
        predict,
        type ="messages"
    )
    demo.launch()