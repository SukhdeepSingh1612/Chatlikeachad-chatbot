import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLAMA3_MODEL = "llama3-70b-8192"

# Validate API key
if not GROQ_API_KEY:
    st.error("Missing GROQ_API_KEY in your .env file.")
    st.stop()

# Streamlit App Setup
st.set_page_config(page_title="LLAMA3 Chatbot", layout="centered")
st.title("🤖 Llama3 Chatbot using Groq API")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to get response from Groq
def generate_response(prompt):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    body = {
        "model": LLAMA3_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            *st.session_state.chat_history,
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=body, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# User input
user_prompt = st.chat_input("Ask me anything...")

if user_prompt:
    # Add user input to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Generate response
    bot_reply = generate_response(user_prompt)

    # Add assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

# Display chat messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
