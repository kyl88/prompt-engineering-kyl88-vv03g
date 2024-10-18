import os
import streamlit as st
from streamlit import session_state as ss
from common import Controller, Quiz, View
from common.genai import Provider, LLM, ModelGateway
from prompts import *
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

st.set_page_config(page_title="Prompt Engineering Mission - Quiz Generator", layout="wide")

# Init SS

if 'current_prompt' not in ss:
    ss.current_prompt = ss.current_prompt = "Zero-shot"

if 'provider' not in ss:
    ss.provider = Provider.GOOGLE

if 'model' not in ss:
    ss.model = LLM.GEMINI_1o5_FLASH


if not os.getenv('GOOGLE_API_KEY'):
    st.error("Please set your API Key as an environment variable for each provider")
    st.caption(f"Supported providers: {[provider.value for provider in Provider]}")
    st.info("You can create a Google AI API key in the AI Studio at https://aistudio.google.com/ for free!")
    st.stop()

# Init Controller with Current Quiz
controller = Controller()
view = View()

# Sidebar for selecting prompting technique
st.sidebar.title("Model Selection")

# Sidebar for selecting provider and model
provider = st.sidebar.selectbox(
    "Select Provider",
    options=[provider for provider in Provider],
    format_func=lambda x: x.value
)

# Model Selection based on the selected provider
supported_models = ModelGateway.provider_model_map[provider]["supported_models"]
model = st.sidebar.selectbox(
    "Select Model",
    options=supported_models,
    format_func=lambda x: x.value
)

# Update session state
ss.provider = provider
ss.model = model

# Sidebar for selecting prompting technique
technique = st.sidebar.selectbox(
    "Select Prompting Technique",
    options=list(PROMPT_TECHNIQUES.keys())
)

# Update current prompt based on selected technique
ss.current_prompt = PROMPT_TECHNIQUES[technique]
ss.current_prompt_name = technique


# Run Main app logic
view.render(controller)
