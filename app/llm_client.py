"""
llm_client.py

Wrapper around Groq Python SDK for generating summaries.
"""

import os
from groq import Groq
import streamlit as st

# Load API key from environment
API_KEY = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY not set in environment.")

# Initialize Groq client
client = Groq(api_key=API_KEY)


def generate_summary(prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    """
    Generate a structured summary using Groq LLM.
    
    Parameters
    ----------
    prompt : str
        The instruction + transcript combined.
    model : str
        Model to use. Default: llama-3.3-70b-versatile
    
    Returns
    -------
    str
        The model's response text.
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an assistant that creates structured meeting summaries."},
            {"role": "user", "content": prompt},
        ],
        model=model,
    )

    return chat_completion.choices[0].message.content
