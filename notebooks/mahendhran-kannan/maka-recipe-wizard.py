import time
import numpy as np
import pandas as pd
import streamlit as st
from src.prompt_setup import prompt_setup
from src.recipe_gen import generate_text
from src.image_gen import generate_image

st.write("AI Recipe Wizard")


user_ingredients = st.text_input("Your magic ingredients for the recipe (e.g., Turmeric, Pepper, Butter)")
prompt =  prompt_setup(user_ingredients)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

def stream_data(mytext):
    for word in mytext.split(" "):
        yield word + " "
        time.sleep(0.02)

st.button('Click for AI Recipe', on_click=click_button)
col1, col2 = st.columns(2)
if st.session_state.clicked:
   
    if len(user_ingredients) > 0:
        #st.write('Button clicked!') 
        from config.secrets import OPENAI_API_KEY #, MK_HF_API_KEY
        from openai import OpenAI

        model =  "gpt-3.5-turbo" # "gpt-4o-mini"
        print(prompt)
        client = OpenAI(
            api_key=OPENAI_API_KEY,
        )
        with st.spinner('Chef is preparing.. Wait for the magic recipe...'):
            time.sleep(5)
            title, ingredients, instructions, summary = generate_text(client, model, user_ingredients)

            image_url = generate_image(client, summary)
    
            with col1:
                st.write(f":male-cook:**Ingredients** :sparkles:")
                st.write_stream(stream_data(ingredients))
                st.write(f":male-cook:**instructions** :sparkles:")
                st.write_stream(stream_data(instructions))
            with col2:
                st.header(f":male-cook:**{title}** :sparkles:")
                st.image(image_url)
                
        st.success("Done!")
    else:
        st.write("Add some ingredients please!")
        st.session_state.clicked = False
        
