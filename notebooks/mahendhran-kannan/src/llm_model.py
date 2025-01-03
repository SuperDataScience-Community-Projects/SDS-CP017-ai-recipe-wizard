from config.secrets import OPENAI_API_KEY, MK_HF_API_KEY
from openai import OpenAI
from src.prompt_setup import prompt_setup
from src.image_gen import generate_image
from src.utils import extract_section
from huggingface_hub import InferenceClient

# Dictionary of LLM models and their corresponding API keys
LLM_MODELS = {
    "gpt-3.5-turbo": {"type": 1, "key": OPENAI_API_KEY},
    "gpt-4o-mini": {"type": 1, "key": OPENAI_API_KEY},
    "meta-llama/Llama-3.3-70B-Instruct": {"type": 2, "key": MK_HF_API_KEY},
    "meta-llama/Llama-2-7b-chat-hf": {"type": 2, "key": MK_HF_API_KEY},
}

llm_role_set = "You are a world-renowned chef"

# Huggingface
def huggingface_connect(_model, _api_key, prompt):

    print("..huggingface_connect.1.")

    client = InferenceClient(api_key=_api_key)
    messages = [
        {
            "role": "user",
            "content": f"{llm_role_set + ' ' + prompt}"
        }
    ]
    completion = client.chat.completions.create(
    model=_model, 
    messages=messages, 
    max_tokens=500
    )
    response = completion.choices[0].message
    print("..huggingface_connect.2..response...")
    print(response)
    return response       
   
   
# OpenAI
def openAI_connect(_model, api_key, prompt):   
    client = OpenAI(
                api_key=api_key,
            )
    response = client.chat.completions.create(
            model=_model,  
            messages=[
                {"role": "system", "content": llm_role_set},
                {"role": "user", "content":prompt}
            ],
            max_tokens=1000,
            temperature=0.7,           
        )

    # Extract recipe content
    recipe_content = response.choices[0].message.content
    return recipe_content

# Use LLM as per choice
def llm_init(_model, user_input):   
    #api_key = LLM_MODELS[_model]  # get key of the selected model
    model_info = LLM_MODELS[_model]
    model_type = model_info["type"]
    api_key = model_info["key"]

    prompt =  prompt_setup(user_input)
    
    if model_type == 1:  
         response = openAI_connect(_model, api_key, prompt)
    elif model_type == 2:      
         response = huggingface_connect(_model, api_key, prompt)
    else:
        return "Invalid option"          
   
    title, ingredients, instructions, image_url = extract_response(response)
    return title, ingredients, instructions, image_url

# Format Output
def extract_response(recipe_content):
       # Extract the sections
        title = extract_section(recipe_content, "Title") 
        ingredients = extract_section(recipe_content, "Ingredients")
        instructions = extract_section(recipe_content, "Instructions")
        summary = extract_section(recipe_content, "Summary")
        image_url = generate_image(summary)        
        return title, ingredients, instructions, image_url   