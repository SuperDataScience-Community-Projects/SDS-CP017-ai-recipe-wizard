import time
import streamlit as st
from src.llm_model import LLM_MODELS, llm_init

# handlers
def click_button():
    st.session_state.clicked = True

def stream_data(mytext):
    for word in mytext.split(" "):
        yield word + " "
        time.sleep(0.02)

# streamlit markups
st.title("AI Recipe Wizard")

# Dropdown to select the LLM model
#st.subheader("Select a LLM Model")
selected_model = st.selectbox("Select a LLM Model", list(LLM_MODELS.keys()))

# User input
user_ingredients = st.text_input("Your magic ingredients for the recipe (e.g., Turmeric, Pepper, Butter)")

# submit button
st.button('Click for AI Recipe', on_click=click_button)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

# show results
col1, col2 = st.columns(2)
if st.session_state.clicked:   
    if len(user_ingredients) > 0:         
        with st.spinner('Chef is preparing.. Wait for the magic recipe...'):
            # LLM call to generate the recipe
            title, ingredients, instructions, image_url = llm_init(selected_model, user_ingredients)        
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
        
