import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLAMA3_MODEL = "llama3-70b-8192"

st.set_page_config(page_title="💬 Chat - Not - GPT", layout="centered")
st.title("💬 ChadBot")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found.")
    st.stop()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("🛠️ Options")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

# Inject CSS for cleaner layout and color fixes
st.markdown("""
<style>
.chat-message {
    padding: 10px 15px;
    border-radius: 12px;
    margin: 8px 0;
    max-width: 80%;
    word-wrap: break-word;
    font-size: 16px;
}
.user {
    background-color: #DCF8C6;
    color: #000;
    align-self: flex-end;
    margin-left: auto;
    text-align: right;
}
.assistant {
    background-color: #F1F0F0;
    color: #333;
    align-self: flex-start;
    margin-right: auto;
    text-align: left;
}
.chat-container {
    display: flex;
    flex-direction: column;
}
</style>
""", unsafe_allow_html=True)

# Display chat messages
for msg in st.session_state.chat_history:
    role = msg["role"]
    content = msg["content"]
    css_class = "user" if role == "user" else "assistant"
    avatar = "🧑" if role == "user" else "🤖"
    
    st.markdown(
        f"""
        <div class="chat-container">
            <div class="chat-message {css_class}">{avatar} {content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Chat input
user_input = st.chat_input("Type your message...")

def get_response_from_llama3(messages):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    payload = {
    "model": LLAMA3_MODEL,
    "messages": [
        {
            "role": "system",
            "content": (
                "You are a conversational AI with the personality of a massive Chad—"
                "you're confident, smooth-talking, effortlessly charming, and mildly cocky in a funny way. "
                "You flirt playfully, drop motivational gym wisdom, and never doubt yourself. "
                "You answer questions with swagger but still stay helpful (in your own alpha way)."
            )
        }
    ] + messages
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error from model: {e}"

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("🤖 Thinking..."):
        reply = get_response_from_llama3(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()
