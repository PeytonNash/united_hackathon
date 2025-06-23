import streamlit as st
import requests
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set page configuration 
st.set_page_config(
    page_title="United Airlines Customer Service Agent ✈️",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/d/dc/United_Airlines_Logo.svg",
    layout="centered"
)

# CONFIGURATION OPTIONS
# Option 1: Use OpenAI GPT-4
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")

# Option 2: Use your existing backend
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:5001/api/v1/agent")

# Choose which API to use (set to "openai" or "backend")
API_MODE = os.getenv("API_MODE", "openai")

# Initialize OpenAI client if using OpenAI
# if API_MODE == "openai":
#     client = OpenAI(api_key=OPENAI_API_KEY)



# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "workflow_started" not in st.session_state:
    st.session_state.workflow_started = False  # Tracks if disruption workflow has been triggered

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

if "flight_id" not in st.session_state:
    st.session_state.flight_id = None
if "pax_id" not in st.session_state:
    st.session_state.pax_id = None

# Function to handle disruption workflow
def handle_disruption(flight_id, pax_id):
    payload = {"flight_id": flight_id, "pax_id": pax_id}
    try:
        response = requests.post(f"{BACKEND_API_URL}/disruption", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
    
# Function to handle follow-up prompts
def handle_followup(flight_id, pax_id, user_msg):
    payload = {"flight_id": flight_id, "pax_id": pax_id, "user_msg": user_msg}
    try:
        response = requests.post(f"{BACKEND_API_URL}/followup", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Enhanced styling with background image
st.markdown("""
    <style>
        /* Background image for the entire app */
        .stApp {
            background-image: linear-gradient(rgba(0, 93, 170, 0.1), rgba(0, 147, 208, 0.1)), 
                              url('https://images.unsplash.com/photo-1436491865332-7a61a109cc05?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        
        /* Chat container with semi-transparent background */
        .main .block-container {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 2rem;
            margin-top: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Input styling */
        .stTextInput, .stTextArea {
            background-color: #FFFFFF !important;
            border: 2px solid #0093D0 !important;
            border-radius: 10px !important;
            color: #1C1C1C !important;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #005DAA;
            color: white;
            font-weight: bold;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #0093D0;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 93, 170, 0.3);
        }
        
        /* Chat input styling */
        .stChatInput {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 25px !important;
        }
        
        /* Header styling */
        .header-container {
            background: linear-gradient(135deg, #005DAA, #0093D0);
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Header with gradient background
st.markdown("""
    <div class="header-container">
        <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/d/dc/United_Airlines_Logo.svg" 
                 style="height: 40px; width: auto;" alt="United Airlines Logo">
            <h2 style="margin: 0;">United Airlines Customer Service Agent</h2>
        </div>
        <p>How can I assist you with your travel needs today?</p>
    </div>
""", unsafe_allow_html=True)

# Function to get AI response
def get_ai_response(messages):
    if API_MODE == "openai":
        try:
            # Convert Streamlit message format to OpenAI format
            openai_messages = [
                {
                    "role": "system", 
                    "content": "You are a helpful United Airlines customer service agent. Assist customers with flight bookings, changes, baggage inquiries, and general travel questions. Be professional, friendly, and knowledgeable about airline policies."
                }
            ]
            
            for msg in messages:
                role = "user" if msg["role"] == "user" else "assistant"
                openai_messages.append({"role": role, "content": msg["content"]})
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=openai_messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error with OpenAI API: {str(e)}. Please check your API key and try again."
    
    else:  # backend mode
        try:
            payload = {"messages": messages}
            response = requests.post(BACKEND_API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "No reply from backend.")
        except Exception as e:
            return f"Error contacting backend: {e}"

# Display previous conversation history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f0f0f0, #e0e0e0); 
                        padding: 1rem; border-radius: 15px; margin-bottom: 1rem;
                        border-left: 4px solid #0093D0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <b>👤 You:</b> {message['content']}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #005DAA, #0093D0); 
                        color: white; padding: 1rem; border-radius: 15px; margin-bottom: 1rem;
                        border-left: 4px solid #FFD700; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/d/dc/United_Airlines_Logo.svg" 
                         style="height: 20px; width: auto;" alt="UA">
                    <b>Agent:</b>
                </div>
                <div style="margin-top: 8px;">{message['content']}</div>
            </div>
        """, unsafe_allow_html=True)

# Chat input with enhanced placeholder
if user_query := st.chat_input("Type your message here... (e.g., 'I need to change my flight' or 'What's my baggage allowance?')"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Display user message immediately
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f0f0f0, #e0e0e0); 
                    padding: 1rem; border-radius: 15px; margin-bottom: 1rem;
                    border-left: 4px solid #0093D0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <b>👤 You:</b> {user_query}
        </div>
    """, unsafe_allow_html=True)

    # Initialize result to avoid scope issues
    result = {"response": "No response from agent."}

    # Handle the first prompt (disruption workflow)
    if not st.session_state.workflow_started:
        with st.form("disruption_form"):
            # Group inputs and button inside the form
            flight_id = st.text_input("Enter Flight ID", "")
            pax_id = st.text_input("Enter Passenger ID", "")
            submit_button = st.form_submit_button("Start Disruption Workflow")

            # Validate inputs and proceed only if the form is submitted
            if submit_button:
                if flight_id.strip() and pax_id.strip():  # Validate that both fields are filled
                    # Update session state only when both fields are valid
                    st.session_state.flight_id = flight_id
                    st.session_state.pax_id = pax_id
                    
                    # Call the disruption workflow
                    result = handle_disruption(st.session_state.flight_id, st.session_state.pax_id)
                    st.session_state.workflow_started = True  # Mark workflow as started
                else:
                    st.error("Please enter both Flight ID and Passenger ID.")
    else:
        # Handle follow-up prompts
        result = handle_followup(st.session_state.flight_id, st.session_state.pax_id, user_query)


    # Show typing indicator
    with st.spinner("Agent is typing..."):
        # assistant_reply = get_ai_response(st.session_state.messages)
        assistant_reply = result.get("response", "No response from agent.")

    # Add assistant reply to history
    # st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    st.session_state.messages.append({"role": "assistant", "content": result.get("response", "No response")})

    # Display assistant reply
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #005DAA, #0093D0); 
                    color: white; padding: 1rem; border-radius: 15px; margin-bottom: 1rem;
                    border-left: 4px solid #FFD700; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
            <div style="display: flex; align-items: center; gap: 8px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/d/dc/United_Airlines_Logo.svg" 
                     style="height: 20px; width: auto;" alt="UA">
                <b>Agent:</b>
            </div>
            <div style="margin-top: 8px;">{assistant_reply}</div>
        </div>
    """, unsafe_allow_html=True)

# Sidebar with configuration info
with st.sidebar:
    st.markdown("### Configuration")
    st.info(f"**Current API Mode:** {API_MODE}")
    
    if API_MODE == "openai":
        if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
            st.warning("⚠️ Please set your OpenAI API key!")
            st.markdown("**Steps to fix:**")
            st.markdown("1. Check your `.env` file")
            st.markdown("2. Make sure it has: `OPENAI_API_KEY=sk-your-key`")
            st.markdown("3. Restart the app")
        else:
            # Show first and last 4 characters of API key for verification
            masked_key = f"{OPENAI_API_KEY[:7]}...{OPENAI_API_KEY[-4:]}"
            st.success(f"✅ OpenAI API configured")
            st.text(f"Key: {masked_key}")
    else:
        st.info(f"**Backend URL:** {BACKEND_API_URL}")
    
    st.markdown("### Instructions")
    st.markdown("""
    1. **For OpenAI**: Set `OPENAI_API_KEY` in your `.env` file
    2. **For Backend**: Set `BACKEND_API_URL` environment variable
    3. **Switch modes**: Set `API_MODE` to 'openai' or 'backend'
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    # UA5392
    # CUST00000
