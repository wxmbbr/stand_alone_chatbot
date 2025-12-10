#!/usr/bin/env python3
"""
BBR Network OpenAI Assistant Chat Application (v2 API Version) - SCROLLING FIX
"""

import streamlit as st
import os
import json
import requests
import base64
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

from audio_recorder_streamlit import audio_recorder
from pypdf import PdfReader
from docx import Document

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="BBR Intelligence",
    page_icon="🏗️",
    layout="wide"
)

# Import config values with environment variable fallback for deployment
try:
    from config import OPENAI_API_KEY, ASSISTANT_ID as CONFIG_ASSISTANT_ID
except ImportError:
    CONFIG_ASSISTANT_ID = None
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Allow override via env; fallback to config or default assistant
ASSISTANT_ID = os.getenv('OPENAI_ASSISTANT_ID_OVERRIDE') or os.getenv('OPENAI_ASSISTANT_ID') or CONFIG_ASSISTANT_ID or "asst_mKMsW8mKPQPzt5rVFBeBB8bu"

# Basic config validation
if not OPENAI_API_KEY:
    st.error("❌ OPENAI_API_KEY environment variable is not set. Please configure it in your Render.com service settings.")
    st.stop()

# Define BBR colors
BBR_BLUE = "#003876"
BBR_LIGHT_BLUE = "#e8f0f9"
BBR_GRAY = "#f8f9fa"
BBR_TEXT = "#333333"

# Session state bootstrapping
if "messages" not in st.session_state:
    st.session_state.messages: List[Dict[str, str]] = []
if "file_context" not in st.session_state:
    st.session_state.file_context: Optional[Dict[str, str]] = None
if "voice_history" not in st.session_state:
    st.session_state.voice_history: List[str] = []

# -------- File upload + voice helpers --------
MAX_UPLOAD_MB = 2


def _extract_text(uploaded_file) -> Optional[str]:
    if uploaded_file is None:
        return None
    size_mb = uploaded_file.size / (1024 * 1024)
    if size_mb > MAX_UPLOAD_MB:
        st.error(f"File too large ({size_mb:.2f} MB). Max {MAX_UPLOAD_MB} MB.")
        return None

    name = uploaded_file.name.lower()
    try:
        if name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(pages)
        if name.endswith(".docx"):
            doc = Document(uploaded_file)
            return "\n".join([p.text for p in doc.paragraphs])
        content = uploaded_file.read()
        try:
            return content.decode("utf-8")
        except Exception:
            return content.decode("latin-1", errors="ignore")
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return None


def _transcribe_audio(audio_bytes: bytes) -> Optional[str]:
    if not audio_bytes:
        return None
    try:
        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        data = {"model": "whisper-1"}
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        resp = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers=headers,
            data=data,
            files=files,
        )
        if resp.status_code != 200:
            st.error(f"Transcription failed: {resp.text}")
            return None
        return resp.json().get("text", "").strip()
    except Exception as e:
        st.error(f"Transcription error: {e}")
        return None

# Function to load and encode image to base64
def get_image_base64(image_path):
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Logo resolution helper
def resolve_logo_path() -> str:
    candidates = [
        "images/BBR_Logo-round.png",
        "images/BBR_Logo_round.png",
        "images/BBR_Logo.png",
    ]
    for p in candidates:
        if Path(p).exists():
            return p
    return candidates[-1]

# Get BBR logo and background image as base64
bbr_logo_path = resolve_logo_path()
ebbr_logo_path = "images/EBBR_logo.png"
user_avatar_path = "images/user.png"
bbr_logo_base64 = get_image_base64(bbr_logo_path)

# For Streamlit avatar, we need to use the direct file path, not base64
assistant_avatar = ebbr_logo_path  # Direct path to image file
user_avatar = user_avatar_path  # Direct path to user avatar image

st.markdown(f"""
<style>
    :root {{
        --bbr-blue: {BBR_BLUE};
        --bbr-blue-dark: #0b2c70;
        --bbr-light: {BBR_LIGHT_BLUE};
        --bbr-gray: {BBR_GRAY};
        --bbr-text: {BBR_TEXT};
        --card: #ffffff;
        --shadow: 0 12px 32px rgba(0,0,0,0.12);
    }}

    body, .stApp {{
        background: linear-gradient(160deg, #f5f7fb 0%, #eef2f8 60%, #f9fbff 100%);
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
        padding: 0 18px 140px 18px !important;
        max-width: 1100px !important;
        margin: 0 auto;
    }}

    .page-header {{
        background: var(--bbr-blue-dark);
        border: none;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
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
        color: #fff;
        font-size: 1.08rem;
        font-weight: 800;
        letter-spacing: 0.01em;
    }}
    .logo-container img {{
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: transparent;
        padding: 0;
        box-shadow: none;
        object-fit: contain;
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
        height: calc(100vh - 240px) !important;
        max-height: calc(100vh - 240px) !important;
        overflow-y: auto !important;
    }}

    .stChatFlow::-webkit-scrollbar {{
        width: 10px;
    }}
    .stChatFlow::-webkit-scrollbar-track {{
        background: #f1f3f9;
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
        box-shadow: 0 4px 18px rgba(0,0,0,0.12);
    }}
    .stChatMessage.assistant [data-testid="stMarkdownContainer"] {{
        background: #ffffff !important;
        border: 1px solid #e4e9f2 !important;
        color: var(--bbr-text) !important;
        border-radius: 14px !important;
        padding: 0.9rem 1rem !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06) !important;
    }}
    .stChatMessage.user [data-testid="stMarkdownContainer"] {{
        background: linear-gradient(135deg, var(--bbr-blue-dark), #002d79) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 14px 14px 6px 14px !important;
        padding: 0.95rem 1.05rem !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.12) !important;
    }}
    .stChatMessage.assistant pre {{
        background: #f8f9fd !important;
        border: 1px solid #e6ebf5 !important;
        border-radius: 10px !important;
        padding: 0.75rem !important;
    }}

    /* Input */
    .stChatFloatingInputContainer {{
        bottom: 18px !important;
        width: 100% !important;
        max-width: 1100px !important;
        margin: 0 auto !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        position: fixed !important;
        z-index: 1001 !important;
        background: rgba(255,255,255,0.94) !important;
        border: 1px solid #dfe6f2 !important;
        border-radius: 14px !important;
        box-shadow: var(--shadow);
        backdrop-filter: blur(10px);
        padding: 10px !important;
    }}
    .stChatInputContainer input {{
        border-radius: 12px !important;
        border: 1px solid #cfd9ec !important;
        padding: 0.9rem 1rem !important;
        background: #f7f9fd !important;
    }}
    .stChatInputContainer button {{
        border-radius: 12px !important;
        background: var(--bbr-blue) !important;
        color: #fff !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }}

    /* Sidebar tweaks */
    section[data-testid="stSidebar"] > div {{
        background: #f9fbff;
        border-right: 1px solid #e7edf6;
    }}

    /* Badges / captions */
    .stCaption {{
        color: #5a6880 !important;
    }}

    /* Emphasis styling */
    .stMarkdown strong,
    .stMarkdown b {{
        color: var(--bbr-blue);
        font-weight: 800;
    }}
    .stMarkdown em,
    .stMarkdown i {{
        color: var(--bbr-blue);
        font-style: normal;
        font-weight: 700;
    }}
    .stMarkdown mark {{
        background: #fff3c4;
        padding: 0 4px;
        border-radius: 4px;
    }}
    .stMarkdown ul li {{
        border-left: 3px solid rgba(0,45,121,0.12);
        padding-left: 10px;
        margin-bottom: 6px;
    }}

    /* Mobile tweaks */
    @media (max-width: 768px) {{
        .page-header {{
            margin: 10px auto 6px auto;
            padding: 0 10px;
            height: 56px;
            border-radius: 12px;
        }}
        .logo-container img {{
            height: 36px;
        }}
        .header-description {{
            font-size: 0.95rem;
        }}
        .block-container {{
            padding: 0 10px 120px 10px !important;
        }}
        .stChatFlow {{
            height: calc(100vh - 240px) !important;
            padding: 12px !important;
        }}
        .stChatMessage {{
            max-width: 100% !important;
            margin: 0.85rem 0 !important;
        }}
        .stChatMessage.assistant [data-testid="stMarkdownContainer"],
        .stChatMessage.user [data-testid="stMarkdownContainer"] {{
            padding: 0.75rem 0.85rem !important;
            font-size: 0.95rem !important;
        }}
        .stChatFloatingInputContainer {{
            bottom: 12px !important;
            padding: 8px !important;
        }}
        .stChatInputContainer input {{
            padding: 0.75rem 0.85rem !important;
            font-size: 0.95rem !important;
        }}
        .stChatInputContainer button {{
            min-height: 40px !important;
            font-size: 0.95rem !important;
        }}
    }}
</style>

<script>
// JAVASCRIPT TO FORCE SCROLLING
document.addEventListener('DOMContentLoaded', function() {{
    function forceScrolling() {{
        // Find the chat flow container
        const chatFlow = document.querySelector('.stChatFlow');
        if (chatFlow) {{
            // Force scrolling properties
            chatFlow.style.overflowY = 'scroll';
            chatFlow.style.overflowX = 'hidden';
            chatFlow.style.height = 'calc(100vh - 200px)';
            chatFlow.style.maxHeight = 'calc(100vh - 200px)';
            
            // Scroll to bottom when new messages appear
            chatFlow.scrollTop = chatFlow.scrollHeight;
        }}
        
        // Also try to find any other potential containers
        const containers = document.querySelectorAll('[data-testid="stChatFlow"], .stChatFlow');
        containers.forEach(container => {{
            container.style.overflowY = 'scroll';
            container.style.overflowX = 'hidden';
            container.style.height = 'calc(100vh - 200px)';
            container.style.maxHeight = 'calc(100vh - 200px)';
        }});
    }}
    
    // Run immediately
    forceScrolling();
    
    // Run every second to catch dynamic changes
    setInterval(forceScrolling, 1000);
    
    // Run when DOM changes
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

# Sidebar inputs
def render_sidebar_inputs():
    with st.sidebar:
        st.subheader("Context & input")

        uploaded = st.file_uploader("Upload file (pdf, docx, txt, <=2MB)", type=["pdf", "docx", "txt"])
        if uploaded:
            text = _extract_text(uploaded)
            if text:
                st.session_state.file_context = {"name": uploaded.name, "text": text[:12000]}
                st.success(f"Loaded {uploaded.name} ({len(text)} chars)")
        if st.session_state.file_context:
            st.info(f"Using context: {st.session_state.file_context['name']}")
            if st.button("Clear context"):
                st.session_state.file_context = None

        st.markdown("---")
        st.caption("Voice input (hold to record)")
        audio_bytes = audio_recorder(text="🎤 Hold to record", pause_threshold=2.0, sample_rate=16000)
        if audio_bytes:
            with st.spinner("Transcribing..."):
                transcript = _transcribe_audio(audio_bytes)
            if transcript:
                st.session_state.voice_history.append(transcript)
                st.success("Voice captured. Sending...")
                process_user_message(transcript)
        if st.session_state.voice_history:
            st.caption("Recent transcripts")
            for t in st.session_state.voice_history[-3:][::-1]:
                st.write(f"• {t}")


def render_mobile_inputs():
    with st.expander("Uploads & voice (mobile)", expanded=False):
        uploaded = st.file_uploader("Upload file (pdf, docx, txt, <=2MB)", type=["pdf", "docx", "txt"], key="mobile_file")
        if uploaded:
            text = _extract_text(uploaded)
            if text:
                st.session_state.file_context = {"name": uploaded.name, "text": text[:12000]}
                st.success(f"Loaded {uploaded.name} ({len(text)} chars)")
        if st.session_state.file_context:
            st.info(f"Using context: {st.session_state.file_context['name']}")
            if st.button("Clear context", key="mobile_clear_context"):
                st.session_state.file_context = None

        st.caption("Voice input (hold to record)")
        audio_bytes = audio_recorder(text="🎤 Hold to record", pause_threshold=2.0, sample_rate=16000, key="mobile_audio")
        if audio_bytes:
            with st.spinner("Transcribing..."):
                transcript = _transcribe_audio(audio_bytes)
            if transcript:
                st.session_state.voice_history.append(transcript)
                st.success("Voice captured. Sending...")
                process_user_message(transcript)
        if st.session_state.voice_history:
            st.caption("Recent transcripts")
            for t in st.session_state.voice_history[-3:][::-1]:
                st.write(f"• {t}")


def render_quick_actions():
    st.markdown("### ")
    actions = st.columns([1, 1], gap="small")
    with actions[0]:
        st.caption("📎 Attach")
        uploaded = st.file_uploader("Attach file", type=["pdf", "docx", "txt"], label_visibility="collapsed", key="inline_file")
        if uploaded:
            text = _extract_text(uploaded)
            if text:
                st.session_state.file_context = {"name": uploaded.name, "text": text[:12000]}
                st.success(f"Loaded {uploaded.name} ({len(text)} chars)")
    with actions[1]:
        st.caption("🎤 Voice")
        audio_bytes = audio_recorder(text="", pause_threshold=2.0, sample_rate=16000, key="inline_audio")
        if audio_bytes:
            with st.spinner("Transcribing..."):
                transcript = _transcribe_audio(audio_bytes)
            if transcript:
                st.session_state.voice_history.append(transcript)
                st.success("Voice captured. Sending...")
                process_user_message(transcript)


def process_user_message(prompt: str):
    if not prompt:
        return
    context = ""
    if st.session_state.file_context:
        ctx = st.session_state.file_context
        context = f"\n\n[File context: {ctx['name']}]\n{ctx['text']}"
    final_prompt = prompt + context

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=assistant_avatar):
        with st.spinner("Thinking..."):
            response = query_openai_assistant(final_prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

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

# Initialize session state defaults
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_message = """Hello! I'm the BBR Intelligence Assistant. How can I help you today? For example, ask:
- “What’s the spec for CMG?” 
- “Weight of CMI trumplate 1206?” 
- “Share docs context” (upload a file in the sidebar or mobile expander)."""
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Create fixed header
st.markdown(f"""
<div class="page-header">
    <div class="logo-container">
        <img src="data:image/png;base64,{bbr_logo_base64}" alt="BBR Logo" style="height: 50px; margin-right: 15px;">
        <div class="header-description">BBR Intelligence</div>
    </div>
</div>
""", unsafe_allow_html=True)

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
    process_user_message(prompt)
elif len(st.session_state.messages) == 1:
    # Auto-start a conversation by posing a gentle opener
    auto_prompt = "Please briefly introduce yourself and how you can help with BBR products and specs."
    process_user_message(auto_prompt)

# Inline quick actions (file attach, voice)
render_quick_actions()