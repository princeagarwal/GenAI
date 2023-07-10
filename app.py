## Importing dependencies
import os
import json
import numpy as np
import pandas as pd
import warnings
import streamlit as st
warnings.filterwarnings('ignore')

from models import generate_speech, generate_speech_bark

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

## Header
st.set_page_config(layout="wide")
st.title("Speech Synthesis Demo:")
# st.subheader("Interface for checking different TTS models tried for the PoC")

## Side-bar Options
st.sidebar.markdown("### Inputs:")
with st.sidebar:
    models_list = ['Azure API', 'Google API', 'Meta MMS', 'Suno Bark']
    selected_models = st.multiselect("API/Model type - ", models_list, models_list[0])

print(selected_models)

n = len(selected_models)

## Input text
input_text = st.text_area('Enter text to speak:', '''input text''')

start_button = st.button('Generate')

if start_button:

    cols = st.columns(n)

    model_configs = {}
    for i, model_type in enumerate(selected_models):
        model_configs[model_type] = config[model_type]

        with cols[i]:

            if model_type == 'Azure API':
                st.header(f"""{model_type} Result:""")
                
                audio_result = generate_speech(model_configs[model_type], input_text)
                st.audio(audio_result)
            
            elif model_type == 'Suno Bark':
                st.header(f"""{model_type} Result:""")
                
                # audio_result = generate_speech_bark(model_configs[model_type], input_text)                
                audio_file = open('bark_generation.wav', 'rb')
                st.audio(audio_file, format='audio/wav')

            elif model_type == 'Google API':
                st.header(f"""{model_type} Result:""")
                
                # audio_result = generate_speech_bark(model_configs[model_type], input_text)                
                st.audio(audio_result)
            
            elif model_type == 'Meta MMS':
                st.header(f"""{model_type} Result:""")
                
                # audio_result = generate_speech_bark(model_configs[model_type], input_text)                
                st.audio(audio_result)
            
