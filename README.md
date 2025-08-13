# BBR Expert Assistant

A chat interface for the BBR Expert Assistant powered by OpenAI's Assistant API.

## Features

- Clean, professional chat interface with BBR branding
- Utilizes OpenAI's Assistant API (v2) for intelligent responses
- Responsive design that works across different screen sizes
- Automatic welcome message to initiate conversation
- Custom avatars for both user and assistant
- Can be embedded in websites via iframe

## Prerequisites

- Python 3.8 or newer
- OpenAI API key with access to the Assistants API
- An existing OpenAI Assistant

## Setup

1. Clone this repository
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venvope
   source venvope/bin/activate  # On Windows: venvope\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `config.py` file based on the `env.example` template:
   ```python
   OPENAI_API_KEY = "your-openai-api-key"
   ASSISTANT_ID = "your-assistant-id"
   ```
5. Ensure you have the necessary image files in the `images` directory:
   - `BBR_Logo.png` - Used for the header
   - `EBBR_logo.png` - Used for the assistant avatar
   - `user.png` - Used for the user avatar

## Running the Application

### Quick Start (Recommended)

Use the simple launcher:

```bash
python3 run.py
```

Choose:
- Option 1: Just the chatbot (http://localhost:8501)
- Option 2: Full web interface (chatbot + website demo)

### Manual Start

To manually start the application:

```bash
python3 -m streamlit run app_streamlit_v2.py --server.port=8501
```

The application will be available at http://localhost:8501

### Embedding in a Website

To embed the chat interface in a website, use an iframe:

```html
<div id="chat-widget">
    <iframe id="chat-frame" src="http://localhost:8501" scrolling="yes" frameborder="0"></iframe>
</div>
```

See the `index_improved.html` file for a complete example of website integration with toggle button and working scrolling.

## Troubleshooting

### Port Already in Use

If you see an error like "Port 8501 is already in use", you can either:

1. Kill all running Streamlit processes:
   ```bash
   pkill -f streamlit
   ```

2. Or specify a different port:
   ```bash
   python3 -m streamlit run app_streamlit_v2.py --server.port=8502
   ```

### Avatar Display Issues

If avatars don't display correctly:

1. Make sure the image paths are correct in `app_streamlit_v2.py`:
   ```python
   bbr_logo_path = "images/BBR_Logo.png"
   ebbr_logo_path = "images/EBBR_logo.png"
   user_avatar_path = "images/user.png"
   ```

2. Ensure the image files exist in the specified locations
3. Use only file paths for avatars, not HTML or base64 encoded images
4. Check that image files are valid and not corrupted

### CSS Syntax Issues

If you encounter Python errors related to CSS syntax:

1. Make sure all CSS braces in f-strings use double braces `{{` and `}}` 
2. Don't use variable names that might conflict with CSS properties
3. Keep CSS selectors simple and avoid complex nested selectors when possible

### Interface Styling and Scrollbar Issues

If the chat interface doesn't look right or scrolling isn't working:

1. The scrollbar is provided by Streamlit's native functionality
2. For long conversations, the scrollbar will appear automatically
3. If the scrollbar isn't visible, try adding more messages to trigger overflow
4. The chat container is intentionally sized to allow for scrolling

## Customization

### Changing Colors

To change the colors, modify these variables at the top of `app_streamlit_v2.py`:

```python
BBR_BLUE = "#003876"
BBR_LIGHT_BLUE = "#e8f0f9"
BBR_GRAY = "#f8f9fa"
BBR_TEXT = "#333333"
```

### Changing Welcome Message

Modify the welcome message in the chat history initialization:

```python
st.session_state.messages = [
    {"role": "assistant", "content": "Your custom welcome message here"}
]
```

## Server Deployment

For production deployment:

1. Host the Streamlit app on a public server with a proper domain
2. Update the iframe src in your website to point to the public URL
3. Ensure CORS headers are properly set to allow iframe embedding
4. Consider using a reverse proxy (Nginx/Apache) for better security

## Security Considerations

1. Store your API key securely and never expose it in client-side code
2. Consider implementing rate limiting to prevent API abuse
3. For production environments, host on a server with HTTPS enabled
4. Implement proper error handling for API failures

## Code Structure

- **app_streamlit_v2.py**: Main application file with UI and API logic
- **run.py**: Launcher script for easier startup
- **config.py**: Configuration settings (API keys, Assistant ID)
- **requirements.txt**: Required Python packages
- **images/**: Directory containing image assets

## Maintenance

1. Regularly update the OpenAI API key if it expires
2. Check for Streamlit updates with `pip install streamlit --upgrade`
3. Test the application after any configuration changes 