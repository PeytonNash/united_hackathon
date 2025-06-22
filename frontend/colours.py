import streamlit as st
import requests
import json
import os

# set page configuration 
st.set_page_config(page_title="United Airlines Customer Service Agent", page_icon="✈️", layout="centered")

# united colours UI theme applied here via CSS injection
st.markdown("""
    <style>
        .stApp {
            background-color: #F5F5F5;
            font-family: 'Inter', sans-serif;
        }
        .block-container {
            padding: 2rem 2rem 2rem 2rem;
        }
        .stTextInput, .stTextArea {
            background-color: #FFFFFF !important;
            border: 2px solid #0093D0 !important;
            border-radius: 10px !important;
            color: #1C1C1C !important;
        }
        .stButton>button {
            background-color: #005DAA;
            color: white;
            font-weight: bold;
            border-radius: 25px;
            padding: 0.5rem 2rem;
        }
        .stButton>button:hover {
            background-color: #0093D0;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("### United Airlines Customer Service Agent")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/United_Airlines_Logo.svg/320px-United_Airlines_Logo.svg.png", width=150)

# CONFIGURABLE BACKEND URL
# change this to our backend URL
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:5001/api/v1/agent")

# initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display previous conversation history sequentially with custom HTML styling (new colours attempt, for multi-turn)
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div style="background-color:#E0E0E0; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                <b>User:</b> {message['content']}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="background-color:#005DAA; color:white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                <b>Agent:</b> {message['content']}
            </div>
        """, unsafe_allow_html=True)

# chat input
if user_query := st.chat_input("Hello! I'm your United Airlines chatbot assistant. How can I help you today?"):
    # add user message to history
    st.session_state.messages.append({"role": "user", "content": user_query})

    # display user message immediately
    st.markdown(f"""
        <div style="background-color:#E0E0E0; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <b>User:</b> {user_query}
        </div>
    """, unsafe_allow_html=True)

    # call backend with full message history
    payload = {
        "messages": st.session_state.messages
    }

    try:
        response = requests.post(BACKEND_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        assistant_reply = data.get("response", "No reply from backend.")
    except Exception as e:
        assistant_reply = f"Error contacting backend: {e}"

    # add assistant reply to history
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    # display assistant reply
    st.markdown(f"""
        <div style="background-color:#005DAA; color:white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <b>Agent:</b> {assistant_reply}
        </div>
    """, unsafe_allow_html=True)
