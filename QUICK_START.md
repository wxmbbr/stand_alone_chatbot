# BBR Network Chatbot - Quick Start Guide

## Overview
This is a web-based chatbot using OpenAI's Assistant API, designed with BBR Network branding and fully functional chat history scrolling.

## Prerequisites
- Python 3.7+
- OpenAI API Key
- OpenAI Assistant ID

## Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Edit `config.py` and add your credentials:
```python
OPENAI_API_KEY = "your-api-key-here"
ASSISTANT_ID = "your-assistant-id-here"
```

### 3. Run the Application

**Option A: Simple Launcher (Recommended)**
```bash
python3 run.py
```
Then choose:
- Option 1: Just the chatbot (http://localhost:8501)
- Option 2: Full web interface (chatbot + website demo)

**Option B: Direct Launch**
```bash
# Just the chatbot
python3 -m streamlit run app_streamlit_v2.py --server.port=8501

# Website demo (run in separate terminal)
python3 -m http.server 8000
```

## Access Points

### Direct Chatbot
- URL: http://localhost:8501
- Features: Full BBR branding, scrolling chat history, custom avatars

### Embedded Demo
- URL: http://localhost:8000/index_improved.html
- Features: Mock BBR website with floating chat widget

## Key Features

### ✅ Working Chat History Scrolling
- **Fixed height chat container** with forced vertical scrolling
- **Custom BBR-branded scrollbar** (blue theme)
- **Auto-scroll to bottom** for new messages
- **Word wrapping** prevents horizontal overflow

### ✅ BBR Network Branding
- Official BBR logo and colors
- Custom user and assistant avatars
- Professional styling matching BBR website

### ✅ OpenAI Assistant Integration
- Uses OpenAI Assistants API v2
- Direct HTTP requests for reliability
- Custom knowledge base integration

## File Structure
```
├── app_streamlit_v2.py          # Main chatbot application (with scrolling fixes)
├── run.py                       # Simple launcher script
├── index.html                   # Basic website demo
├── index_improved.html          # Advanced website with chat widget
├── config.py                    # API configuration
├── requirements.txt             # Python dependencies
├── images/                      # Logo and avatar images
│   ├── BBR_Logo.png
│   ├── EBBR_logo.png
│   └── user.png
└── README.md                    # Detailed documentation
```

## Troubleshooting

### Port Already in Use
```bash
# Stop existing servers
pkill -f streamlit
pkill -f "http.server"

# Or use different ports
python3 -m streamlit run app_streamlit_v2.py --server.port=8502
```

### Missing Dependencies
```bash
pip install streamlit openai python-dotenv requests
```

### API Connection Issues
1. Verify your `config.py` has correct API key and Assistant ID
2. Check internet connection
3. Ensure OpenAI account has sufficient credits

### Scrolling Issues
The current version (`app_streamlit_v2.py`) includes comprehensive scrolling fixes:
- If scrolling doesn't work, try refreshing the browser
- Clear browser cache if needed
- The scrollbar should be visible and functional

## Server Management

### Start Servers
```bash
python3 run.py  # Interactive launcher
```

### Stop Servers
```bash
# Graceful stop (Ctrl+C in terminal)
# Or force stop all:
pkill -f streamlit && pkill -f "http.server"
```

### Check Running Servers
```bash
# Check what's using port 8501
lsof -i :8501

# Check what's using port 8000  
lsof -i :8000
```

## Support
- Check `README.md` for detailed documentation
- Verify all image files exist in `images/` directory
- Ensure `config.py` contains valid API credentials 