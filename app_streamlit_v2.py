#!/usr/bin/env python3
"""
BBR Network OpenAI Assistant Chat Application (v2 API Version) - SCROLLING FIX
"""

import streamlit as st
import os
import json
import requests
import base64
import secrets
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from supabase_client import (
    get_client as get_supabase_client,
    get_user_by_email,
    create_user,
    count_admins,
    get_invite,
    mark_invite_used,
    create_invite,
    list_invites,
    create_session,
    touch_session,
    touch_last_login,
    save_message,
    fetch_messages,
)

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="BBR Intelligence - Web Assistant",
    page_icon="🏗️",
    layout="wide"
)

# Import config values with environment variable fallback for deployment
try:
    from config import (
        OPENAI_API_KEY,
        ASSISTANT_ID,
        SUPABASE_URL,
        SUPABASE_ANON_KEY,
        SUPABASE_SERVICE_ROLE_KEY,
    )
except ImportError:
    # Fallback to environment variables for deployment
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Basic config validation
if not OPENAI_API_KEY:
    st.error("❌ OPENAI_API_KEY environment variable is not set.")
    st.stop()

if not ASSISTANT_ID:
    st.error("❌ OPENAI_ASSISTANT_ID environment variable is not set.")
    st.stop()

if not SUPABASE_URL or not (SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY):
    st.error("❌ Supabase configuration missing. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY (preferred) or SUPABASE_ANON_KEY.")
    st.stop()

# Cached Supabase client (server-side only)
@st.cache_resource
def supabase_client():
    return get_supabase_client()

# Session state bootstrapping
if "auth_user" not in st.session_state:
    st.session_state.auth_user: Optional[Dict[str, Any]] = None

if "session_id" not in st.session_state:
    st.session_state.session_id: Optional[str] = None

if "messages" not in st.session_state:
    st.session_state.messages: List[Dict[str, str]] = []

# Define BBR colors
BBR_BLUE = "#003876"
BBR_LIGHT_BLUE = "#e8f0f9"
BBR_GRAY = "#f8f9fa"
BBR_TEXT = "#333333"

# Invite-only auth and persistence helpers
def bootstrap_user(email: str, token: str):
    client = supabase_client()
    invite = get_invite(client, token)
    if not invite:
        return None, "Invalid or expired invite token."

    user = get_user_by_email(client, email)
    if not user:
        role = "admin" if count_admins(client) == 0 else "member"
        user = create_user(client, email=email, role=role)
    else:
        touch_last_login(client, user_id=user["id"])

    mark_invite_used(client, invite["id"], user["id"])
    session = create_session(client, user["id"], client_info="streamlit")

    st.session_state.auth_user = user
    st.session_state.session_id = session["id"]

    # preload history (likely empty) and add welcome if empty
    history = fetch_messages(client, session["id"], limit=50)
    if history:
        st.session_state.messages = [{"role": m["role"], "content": m["content"]} for m in history]
    else:
        welcome = """Hello! I'm the BBR Service Assistant. I'm here to help you with information about BBR Network's technologies, applications, and services.

Feel free to copy and paste this message for your inquiry related to ETAs. If you need further assistance or more specific information, please let me know!

How can I assist you today?"""
        st.session_state.messages = [{"role": "assistant", "content": welcome}]
        save_message(client, session["id"], None, "assistant", welcome)

    return user, None


def persist_message(role: str, content: str):
    client = supabase_client()
    session_id = st.session_state.session_id
    user_id = st.session_state.auth_user["id"] if st.session_state.auth_user else None
    if not session_id:
        return
    try:
        save_message(client, session_id, user_id if role == "user" else None, role, content)
        touch_session(client, session_id)
    except Exception:
        st.warning("Message saved locally but failed to persist to Supabase.")


def render_auth_gate():
    st.markdown("### Invite-only access")
    st.caption("Enter your email and invite code to continue.")
    with st.form("auth_form"):
        email = st.text_input("Work email")
        token = st.text_input("Invite code / token")
        submitted = st.form_submit_button("Enter", type="primary")
    if submitted:
        with st.spinner("Validating invite..."):
            user, err = bootstrap_user(email.strip(), token.strip())
        if err:
            st.error(err)
        else:
            st.success(f"Welcome {user['email']}!")


def render_admin_panel():
    user = st.session_state.auth_user
    if not user or user.get("role") != "admin":
        return
    client = supabase_client()
    with st.expander("Admin: manage invites"):
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Invite email (optional)", key="admin_invite_email")
            days = st.number_input("Valid for days", min_value=1, max_value=90, value=7, key="admin_invite_days")
            if st.button("Create invite", key="admin_invite_create", type="primary"):
                with st.spinner("Creating invite..."):
                    invite = create_invite(client, email or None, int(days), issued_by=user["id"])
                st.success(f"Invite created. Token: {invite['token']}")
        with col2:
            invites = list_invites(client, limit=10)
            st.write("Recent invites")
            for inv in invites:
                status = "used" if inv.get("used_at") else "open"
                st.code(f"{inv['token']} ({status}) email={inv.get('email','-')}", language="text")

# Function to load and encode image to base64
def get_image_base64(image_path):
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Get BBR logo and background image as base64
bbr_logo_path = "images/BBR_Logo.png"
ebbr_logo_path = "images/EBBR_logo.png"
user_avatar_path = "images/user.png"
bbr_logo_base64 = get_image_base64(bbr_logo_path)

# For Streamlit avatar, we need to use the direct file path, not base64
assistant_avatar = ebbr_logo_path  # Direct path to image file
user_avatar = user_avatar_path  # Direct path to user avatar image

# Refined UI styling
st.markdown(f"""
<style>
    :root {{
        --bbr-blue: {BBR_BLUE};
        --bbr-light: {BBR_LIGHT_BLUE};
        --bbr-gray: {BBR_GRAY};
        --bbr-text: {BBR_TEXT};
        --card: #ffffff;
        --shadow: 0 10px 40px rgba(0,0,0,0.08);
    }}

    body, .stApp {{
        background: radial-gradient(circle at 20% 20%, #e9f1ff 0%, #f7fbff 28%, #eef3fa 60%, #ffffff 100%);
        color: var(--bbr-text);
    }}

    header, [data-testid="stHeader"], [data-testid="stToolbar"] {{
        display: none !important;
    }}

    .main {{
        max-width: 1200px !important;
        padding: 0 !important;
        margin: 0 auto !important;
    }}

    .block-container {{
        padding: 0 18px 120px 18px !important;
        max-width: 1100px !important;
        margin: 0 auto;
    }}

    .page-header {{
        background: rgba(255,255,255,0.9);
        border: 1px solid #e8eef5;
        box-shadow: var(--shadow);
        height: 70px;
        border-radius: 14px;
        width: 100%;
        display: flex;
        align-items: center;
        padding: 0 18px;
        margin: 18px auto 12px auto;
        position: sticky;
        top: 10px;
        z-index: 1000;
        backdrop-filter: blur(8px);
    }}

    .logo-container {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .header-description {{
        color: var(--bbr-blue);
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }}

    /* Chat area */
    .stChatFlow {{
        border: none !important;
        border-radius: 16px !important;
        max-width: 100% !important;
        width: 100% !important;
        margin: 0 auto 18px auto !important;
        padding: 18px !important;
        background: var(--card);
        box-shadow: var(--shadow);
        height: calc(100vh - 220px) !important;
        max-height: calc(100vh - 220px) !important;
        overflow-y: auto !important;
    }}

    .stChatFlow::-webkit-scrollbar {{
        width: 10px;
    }}
    .stChatFlow::-webkit-scrollbar-track {{
        background: #f3f6fb;
        border-radius: 999px;
    }}
    .stChatFlow::-webkit-scrollbar-thumb {{
        background: var(--bbr-blue);
        border-radius: 999px;
    }}

    /* Messages */
    .stChatMessage {{
        max-width: 90% !important;
        margin: 1rem 0 !important;
        gap: 12px !important;
    }}
    .stChatMessage .stAvatar {{
        box-shadow: 0 4px 18px rgba(0,0,0,0.1);
    }}
    .stChatMessage.assistant [data-testid="stMarkdownContainer"] {{
        background: #f6f8fb !important;
        border: 1px solid #e4e9f2 !important;
        color: var(--bbr-text) !important;
        border-radius: 14px !important;
        padding: 0.9rem 1rem !important;
        box-shadow: none !important;
    }}
    .stChatMessage.user [data-testid="stMarkdownContainer"] {{
        background: linear-gradient(135deg, var(--bbr-blue), #003060) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 14px 14px 4px 14px !important;
        padding: 0.9rem 1rem !important;
        box-shadow: none !important;
    }}
    .stChatMessage.assistant pre {{
        background: #fff !important;
        border: 1px solid #e6ebf5 !important;
        border-radius: 10px !important;
        padding: 0.75rem !important;
    }}

    /* Input */
    .stChatFloatingInputContainer {{
        bottom: 16px !important;
        width: 100% !important;
        max-width: 1100px !important;
        margin: 0 auto !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        position: fixed !important;
        z-index: 1001 !important;
        background: rgba(255,255,255,0.92) !important;
        border: 1px solid #e7edf6 !important;
        border-radius: 14px !important;
        box-shadow: var(--shadow);
        backdrop-filter: blur(8px);
        padding: 10px !important;
    }}
    .stChatInputContainer input {{
        border-radius: 12px !important;
        border: 1px solid #d8e2f2 !important;
        padding: 0.85rem 1rem !important;
        background: #f9fbff !important;
    }}
    .stChatInputContainer button {{
        border-radius: 12px !important;
        background: var(--bbr-blue) !important;
        color: #fff !important;
    }}

    /* Badges / captions */
    .stCaption {{
        color: #5a6880 !important;
    }}

    /* Mobile tweaks */
    @media (max-width: 768px) {{
        .page-header {{
            margin: 12px auto 8px auto;
            padding: 0 12px;
        }}
        .block-container {{
            padding: 0 12px 120px 12px !important;
        }}
        .stChatFlow {{
            height: calc(100vh - 240px) !important;
            padding: 14px !important;
        }}
        .stChatMessage {{
            max-width: 100% !important;
        }}
    }}
</style>

<script>
// Smooth auto-scroll helper
document.addEventListener('DOMContentLoaded', function() {{
    function forceScrolling() {{
        const containers = document.querySelectorAll('[data-testid="stChatFlow"], .stChatFlow');
        containers.forEach(container => {{
            container.style.overflowY = 'auto';
            container.style.overflowX = 'hidden';
            container.scrollTop = container.scrollHeight;
        }});
    }}
    forceScrolling();
    setInterval(forceScrolling, 800);
    const observer = new MutationObserver(forceScrolling);
    observer.observe(document.body, {{ childList: true, subtree: true }});
}});
</script>
""", unsafe_allow_html=True)

# Direct API implementation using v2 of the API
def query_openai_assistant(user_query):
    """
    Query the OpenAI assistant using direct HTTP requests with v2 API.
    """
    try:
        # Step 1: Create a thread
        thread_response = requests.post(
            "https://api.openai.com/v1/threads",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
                "OpenAI-Beta": "assistants=v2"  # Using v2 API
            },
            json={}
        )
        
        if thread_response.status_code != 200:
            return f"Error creating thread: {thread_response.status_code} - {thread_response.text}"
        
        thread_id = thread_response.json()["id"]
        
        # Step 2: Add user message to thread
        message_response = requests.post(
            f"https://api.openai.com/v1/threads/{thread_id}/messages",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
                "OpenAI-Beta": "assistants=v2"
            },
            json={
                "role": "user",
                "content": user_query
            }
        )
        
        if message_response.status_code != 200:
            return f"Error adding message: {message_response.status_code} - {message_response.text}"
        
        # Step 3: Create run
        run_response = requests.post(
            f"https://api.openai.com/v1/threads/{thread_id}/runs",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
                "OpenAI-Beta": "assistants=v2"
            },
            json={
                "assistant_id": ASSISTANT_ID
            }
        )
        
        if run_response.status_code != 200:
            return f"Error creating run: {run_response.status_code} - {run_response.text}"
        
        run_id = run_response.json()["id"]
        
        # Step 4: Poll for completion
        import time
        max_attempts = 30  # 30 seconds max
        for attempt in range(max_attempts):
            run_status_response = requests.get(
                f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "OpenAI-Beta": "assistants=v2"
                }
            )
            
            if run_status_response.status_code != 200:
                return f"Error checking run status: {run_status_response.status_code} - {run_status_response.text}"
            
            run_status = run_status_response.json()["status"]
            
            if run_status == "completed":
                break
            elif run_status in ["failed", "cancelled", "expired"]:
                return f"Run failed with status: {run_status}"
            
            time.sleep(1)  # Wait 1 second before next check
        else:
            return "Timeout waiting for assistant response"
        
        # Step 5: Get messages
        messages_response = requests.get(
            f"https://api.openai.com/v1/threads/{thread_id}/messages",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "OpenAI-Beta": "assistants=v2"
            }
        )
        
        if messages_response.status_code != 200:
            return f"Error retrieving messages: {messages_response.status_code} - {messages_response.text}"
        
        messages = messages_response.json()["data"]
        
        # Get the assistant's latest response
        for message in messages:
            if message["role"] == "assistant":
                content = message["content"][0]
                if content["type"] == "text":
                    return content["text"]["value"]
        
        return "No response from assistant"
        
    except Exception as e:
        return f"Error querying assistant: {str(e)}"

# Require authentication before showing chat
if not st.session_state.auth_user:
    st.markdown(f"""
    <div class="page-header">
        <div class="logo-container">
            <img src="data:image/png;base64,{bbr_logo_base64}" alt="BBR Logo" style="height: 50px; margin-right: 15px;">
            <div class="header-description">BBR Service Assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    render_auth_gate()
    st.stop()

# Create fixed header
st.markdown(f"""
<div class="page-header">
    <div class="logo-container">
        <img src="data:image/png;base64,{bbr_logo_base64}" alt="BBR Logo" style="height: 50px; margin-right: 15px;">
        <div class="header-description">BBR Service Assistant</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Admin tools (invite management)
render_admin_panel()

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"], avatar=user_avatar):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"], avatar=assistant_avatar):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about BBR technologies..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    persist_message("user", prompt)
    
    # Display user message
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant", avatar=assistant_avatar):
        with st.spinner("Thinking..."):
            response = query_openai_assistant(prompt)
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    persist_message("assistant", response)
    
    # Auto-scroll to bottom using JavaScript
    st.markdown("""
    <script>
    setTimeout(function() {
        const chatFlow = document.querySelector('.stChatFlow');
        if (chatFlow) {
            chatFlow.scrollTop = chatFlow.scrollHeight;
        }
    }, 100);
    </script>
    """, unsafe_allow_html=True) 