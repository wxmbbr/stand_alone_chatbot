#!/usr/bin/env python3
"""
BBR Network OpenAI Assistant Chat Application - Render.com Optimized Version
"""

import streamlit as st
import os
import json
import requests
import base64
from datetime import datetime

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="BBR Intelligence - Web Assistant",
    page_icon="🏗️",
    layout="wide"
)

# Import config values with environment variable fallback for deployment
try:
    from config import OPENAI_API_KEY, ASSISTANT_ID
    st.success("✅ Using local config.py")
except ImportError:
    # Fallback to environment variables for deployment
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ASSISTANT_ID = os.getenv('OPENAI_ASSISTANT_ID')
    
    # Debug info
    st.info(f"🔧 Running on Render.com - Environment variables loaded")
    
    # Check if environment variables are set
    if not OPENAI_API_KEY:
        st.error("❌ OPENAI_API_KEY environment variable is not set. Please configure it in your Render.com service settings.")
        st.stop()
    
    if not ASSISTANT_ID:
        st.error("❌ OPENAI_ASSISTANT_ID environment variable is not set. Please configure it in your Render.com service settings.")
        st.stop()

# Define BBR colors
BBR_BLUE = "#003876"
BBR_LIGHT_BLUE = "#e8f0f9"
BBR_GRAY = "#f8f9fa"
BBR_TEXT = "#333333"

# Function to safely load images
def get_image_base64_safe(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        else:
            st.warning(f"⚠️ Image not found: {image_path}")
            return None
    except Exception as e:
        st.warning(f"⚠️ Error loading image {image_path}: {str(e)}")
        return None

# Try to load images (gracefully handle missing images)
bbr_logo_path = "images/BBR_Logo.png"
ebbr_logo_path = "images/EBBR_logo.png"
user_avatar_path = "images/user.png"

# Check if images directory exists
images_exist = os.path.exists("images/")
st.info(f"📁 Images directory exists: {images_exist}")

if images_exist:
    bbr_logo_base64 = get_image_base64_safe(bbr_logo_path)
    assistant_avatar = ebbr_logo_path if os.path.exists(ebbr_logo_path) else None
    user_avatar = user_avatar_path if os.path.exists(user_avatar_path) else None
else:
    bbr_logo_base64 = None
    assistant_avatar = None
    user_avatar = None
    st.warning("📁 Images directory not found - running without images")

# Minimal CSS for basic styling
st.markdown(f"""
<style>
    /* Basic BBR Styling */
    .main {{
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }}
    
    .stChatMessage {{
        margin-bottom: 1rem;
    }}
    
    /* BBR Header */
    .bbr-header {{
        background: linear-gradient(135deg, {BBR_BLUE} 0%, #004c9e 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }}
    
    .bbr-title {{
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }}
    
    .bbr-subtitle {{
        font-size: 14px;
        opacity: 0.9;
    }}
</style>
""", unsafe_allow_html=True)

# Header with conditional logo
header_content = f"""
<div class="bbr-header">
    <div class="bbr-title">🏗️ BBR Intelligence Assistant</div>
    <div class="bbr-subtitle">Your Expert Construction & Engineering Assistant</div>
</div>
"""

if bbr_logo_base64:
    header_content = f"""
    <div class="bbr-header">
        <img src="data:image/png;base64,{bbr_logo_base64}" style="height: 50px; margin-bottom: 10px;">
        <div class="bbr-title">BBR Intelligence Assistant</div>
        <div class="bbr-subtitle">Your Expert Construction & Engineering Assistant</div>
    </div>
    """

st.markdown(header_content, unsafe_allow_html=True)

# OpenAI API functions
def create_thread():
    """Create a new conversation thread"""
    try:
        url = "https://api.openai.com/v1/threads"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2"
        }
        
        response = requests.post(url, headers=headers, json={})
        response.raise_for_status()
        
        thread_data = response.json()
        return thread_data["id"]
    except Exception as e:
        st.error(f"Error creating thread: {str(e)}")
        return None

def add_message_to_thread(thread_id, message):
    """Add a user message to the thread"""
    try:
        url = f"https://api.openai.com/v1/threads/{thread_id}/messages"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2"
        }
        
        data = {
            "role": "user",
            "content": message
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Error adding message: {str(e)}")
        return False

def run_assistant(thread_id):
    """Run the assistant on the thread"""
    try:
        url = f"https://api.openai.com/v1/threads/{thread_id}/runs"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2"
        }
        
        data = {
            "assistant_id": ASSISTANT_ID
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        run_data = response.json()
        return run_data["id"]
    except Exception as e:
        st.error(f"Error running assistant: {str(e)}")
        return None

def get_run_status(thread_id, run_id):
    """Check the status of an assistant run"""
    try:
        url = f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "assistants=v2"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        run_data = response.json()
        return run_data["status"]
    except Exception as e:
        st.error(f"Error getting run status: {str(e)}")
        return None

def get_thread_messages(thread_id):
    """Get all messages from the thread"""
    try:
        url = f"https://api.openai.com/v1/threads/{thread_id}/messages"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "assistants=v2"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        messages_data = response.json()
        return messages_data["data"]
    except Exception as e:
        st.error(f"Error getting messages: {str(e)}")
        return []

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm the BBR Intelligence Assistant. How can I help you with your construction and engineering questions today?"}
    ]

if "thread_id" not in st.session_state:
    with st.spinner("Initializing chat..."):
        st.session_state.thread_id = create_thread()
        if not st.session_state.thread_id:
            st.error("❌ Failed to initialize chat. Please refresh the page.")
            st.stop()

# Display chat messages
for message in st.session_state.messages:
    avatar = None
    if message["role"] == "assistant" and assistant_avatar:
        avatar = assistant_avatar
    elif message["role"] == "user" and user_avatar:
        avatar = user_avatar
    
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about construction, engineering, or BBR services..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant", avatar=assistant_avatar):
        with st.spinner("Thinking..."):
            # Add message to thread
            if add_message_to_thread(st.session_state.thread_id, prompt):
                # Run assistant
                run_id = run_assistant(st.session_state.thread_id)
                
                if run_id:
                    # Wait for completion
                    import time
                    max_wait = 30  # Maximum wait time in seconds
                    waited = 0
                    
                    while waited < max_wait:
                        status = get_run_status(st.session_state.thread_id, run_id)
                        
                        if status == "completed":
                            break
                        elif status in ["failed", "cancelled", "expired"]:
                            st.error(f"❌ Assistant run {status}")
                            break
                        
                        time.sleep(1)
                        waited += 1
                    
                    if status == "completed":
                        # Get the latest messages
                        messages = get_thread_messages(st.session_state.thread_id)
                        
                        if messages:
                            # Get the latest assistant message
                            latest_message = messages[0]
                            if latest_message["role"] == "assistant":
                                content = latest_message["content"][0]["text"]["value"]
                                st.markdown(content)
                                st.session_state.messages.append({"role": "assistant", "content": content})
                            else:
                                st.error("❌ No assistant response found")
                        else:
                            st.error("❌ No messages retrieved")
                    else:
                        st.error("❌ Assistant response timed out")
                else:
                    st.error("❌ Failed to run assistant")
            else:
                st.error("❌ Failed to send message")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: {BBR_TEXT}; font-size: 12px; margin-top: 20px;">
    <p>🏗️ BBR Intelligence Assistant | Powered by OpenAI</p>
    <p>For technical support, visit <a href="https://www.bbrnetwork.com" target="_blank">bbrnetwork.com</a></p>
</div>
""", unsafe_allow_html=True)

# Debug info (only show in development)
if os.getenv('RENDER') != 'true':  # Only show locally, not on Render
    with st.expander("🔧 Debug Info"):
        st.write(f"Thread ID: {st.session_state.get('thread_id', 'Not set')}")
        st.write(f"Images directory exists: {os.path.exists('images/')}")
        st.write(f"BBR Logo exists: {os.path.exists(bbr_logo_path) if bbr_logo_path else 'N/A'}")
        st.write(f"Assistant avatar: {assistant_avatar}")
        st.write(f"User avatar: {user_avatar}")
        st.write(f"Environment: {'Render.com' if os.getenv('RENDER') else 'Local'}")
