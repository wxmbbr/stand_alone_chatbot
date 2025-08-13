# Website Integration Guide - BBR Chatbot

## 🎯 How to Add the BBR Chatbot to Any Existing Website

This guide shows you how to integrate the BBR chatbot into your existing homepage or any website.

## 📋 Prerequisites

1. **Deployed Chatbot**: Your chatbot should be running on Render.com (or another platform)
2. **Chatbot URL**: You'll need your deployed chatbot URL (e.g., `https://your-service-name.onrender.com`)
3. **Website Access**: Ability to edit your existing website's HTML/CSS/JavaScript

## 🚀 Quick Integration (3 Steps)

### Step 1: Add CSS Styles
Add this CSS to your website's `<head>` section or CSS file:

```html
<style>
/* BBR Chatbot Widget Styles */
.bbr-chat-widget {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 400px;
    height: 600px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0,56,118,0.2);
    display: none;
    z-index: 1000;
    font-family: Arial, sans-serif;
}

.bbr-chat-header {
    background: linear-gradient(135deg, #003876 0%, #004c9e 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 12px 12px 0 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 500;
}

.bbr-chat-close-btn {
    background: none;
    border: none;
    color: white;
    font-size: 20px;
    cursor: pointer;
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background-color 0.2s;
}

.bbr-chat-close-btn:hover {
    background-color: rgba(255, 255, 255, 0.2);
}

.bbr-chat-frame {
    width: 100%;
    height: calc(100% - 50px);
    border: none;
    border-radius: 0 0 12px 12px;
    overflow: auto;
    background-color: white;
}

.bbr-chat-toggle {
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 12px 24px;
    background-color: #003876;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-family: Arial, sans-serif;
    font-size: 14px;
    font-weight: 500;
    z-index: 1001;
    box-shadow: 0 3px 12px rgba(0,56,118,0.3);
    transition: all 0.3s ease;
}

.bbr-chat-toggle:hover {
    background-color: #004c9e;
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0,56,118,0.4);
}

/* Responsive Design */
@media (max-width: 480px) {
    .bbr-chat-widget {
        width: 90vw;
        height: 80vh;
        bottom: 10px;
        right: 5vw;
    }
    
    .bbr-chat-toggle {
        bottom: 10px;
        right: 10px;
        padding: 10px 20px;
        font-size: 13px;
    }
}
</style>
```

### Step 2: Add HTML Elements
Add this HTML code anywhere in your website's `<body>` section (preferably at the bottom):

```html
<!-- BBR Chatbot Widget -->
<div class="bbr-chat-widget" id="bbr-chat-widget">
    <!-- Chat Header -->
    <div class="bbr-chat-header">
        <span>💬 BBR Intelligence Assistant</span>
        <button class="bbr-chat-close-btn" id="bbr-chat-close-btn">✕</button>
    </div>
    
    <!-- Chatbot Frame -->
    <iframe class="bbr-chat-frame" 
            id="bbr-chat-frame"
            src="https://your-service-name.onrender.com"
            frameborder="0" 
            scrolling="yes"
            allow="microphone; camera">
    </iframe>
</div>

<!-- Chat Toggle Button -->
<button class="bbr-chat-toggle" id="bbr-chat-toggle">
    💬 Chat with BBR Expert
</button>
```

**⚠️ IMPORTANT**: Replace `https://your-service-name.onrender.com` with your actual Render.com URL!

### Step 3: Add JavaScript Functionality
Add this JavaScript code before the closing `</body>` tag:

```html
<script>
// BBR Chatbot Widget Functionality
(function() {
    const chatToggle = document.getElementById('bbr-chat-toggle');
    const chatWidget = document.getElementById('bbr-chat-widget');
    const chatCloseBtn = document.getElementById('bbr-chat-close-btn');
    const chatFrame = document.getElementById('bbr-chat-frame');
    
    let isOpen = false;
    let isLoaded = false;
    
    function toggleChat() {
        isOpen = !isOpen;
        
        if (isOpen) {
            chatWidget.style.display = 'block';
            chatToggle.style.display = 'none';
            
            // Focus the iframe for accessibility
            setTimeout(() => {
                chatFrame.focus();
            }, 100);
        } else {
            chatWidget.style.display = 'none';
            chatToggle.style.display = 'block';
        }
    }
    
    // Event listeners
    chatToggle.addEventListener('click', toggleChat);
    chatCloseBtn.addEventListener('click', toggleChat);
    
    // Handle iframe loading
    chatFrame.addEventListener('load', () => {
        isLoaded = true;
    });
    
    // Close chat when clicking outside (optional)
    document.addEventListener('click', (e) => {
        if (isOpen && !chatWidget.contains(e.target) && e.target !== chatToggle) {
            toggleChat();
        }
    });
    
    // Keyboard shortcut (ESC to close)
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isOpen) {
            toggleChat();
        }
    });
})();
</script>
```

## 🎨 Customization Options

### Change Position
To move the chatbot to the left side:
```css
.bbr-chat-widget, .bbr-chat-toggle {
    left: 20px;  /* Instead of right: 20px */
    right: auto;
}
```

### Change Size
```css
.bbr-chat-widget {
    width: 350px;    /* Smaller width */
    height: 500px;   /* Smaller height */
}
```

### Change Colors
```css
.bbr-chat-header {
    background: linear-gradient(135deg, #your-color 0%, #your-color2 100%);
}

.bbr-chat-toggle {
    background-color: #your-color;
}
```

### Custom Button Text
```html
<button class="bbr-chat-toggle" id="bbr-chat-toggle">
    🤖 Ask Our Expert  <!-- Your custom text -->
</button>
```

## 🔧 Advanced Integration

### For WordPress
1. Go to **Appearance > Theme Editor**
2. Edit your theme's `functions.php` file
3. Add this code:

```php
function add_bbr_chatbot() {
    // Add the CSS, HTML, and JavaScript from above
    echo '<style>/* CSS from Step 1 */</style>';
    echo '<!-- HTML from Step 2 -->';
    echo '<script>/* JavaScript from Step 3 */</script>';
}
add_action('wp_footer', 'add_bbr_chatbot');
```

### For React/Next.js
Create a component:

```jsx
// components/BBRChatbot.js
import { useState, useEffect } from 'react';

const BBRChatbot = () => {
    const [isOpen, setIsOpen] = useState(false);
    
    return (
        <>
            {/* Chat Widget */}
            {isOpen && (
                <div className="bbr-chat-widget">
                    <div className="bbr-chat-header">
                        <span>💬 BBR Intelligence Assistant</span>
                        <button onClick={() => setIsOpen(false)}>✕</button>
                    </div>
                    <iframe 
                        src="https://your-service-name.onrender.com"
                        className="bbr-chat-frame"
                        frameBorder="0"
                        allow="microphone; camera"
                    />
                </div>
            )}
            
            {/* Toggle Button */}
            {!isOpen && (
                <button 
                    className="bbr-chat-toggle"
                    onClick={() => setIsOpen(true)}
                >
                    💬 Chat with BBR Expert
                </button>
            )}
        </>
    );
};

export default BBRChatbot;
```

## 🚨 Important Notes

### URL Configuration
- **Development**: Use `http://localhost:8501`
- **Production**: Use your Render.com URL: `https://your-service-name.onrender.com`

### Security Considerations
- The iframe loads external content
- Ensure your chatbot URL uses HTTPS in production
- Consider implementing Content Security Policy (CSP) if needed

### Performance
- The iframe loads when the page loads (consider lazy loading for better performance)
- The chatbot starts hidden to avoid impacting page load speed

## 🎯 Testing

1. **Load your website**
2. **Click the chat button** - Widget should open
3. **Test the chatbot** - Should load and respond
4. **Test closing** - Click X or outside the widget
5. **Test responsiveness** - Check on mobile devices

## 🔧 Troubleshooting

### Chatbot doesn't load
- Check your Render.com URL is correct and accessible
- Verify the service is running on Render.com
- Check browser console for errors

### Widget doesn't appear
- Ensure CSS is loaded
- Check for JavaScript errors in browser console
- Verify HTML elements have correct IDs

### Styling conflicts
- Use more specific CSS selectors
- Add `!important` to critical styles
- Check for CSS conflicts with existing website styles

## 📱 Mobile Optimization

The provided CSS includes responsive design, but you may need to adjust:

```css
@media (max-width: 768px) {
    .bbr-chat-widget {
        width: 95vw;
        height: 90vh;
        bottom: 0;
        right: 2.5vw;
        border-radius: 12px 12px 0 0;
    }
}
```

## 🎉 That's It!

Your BBR chatbot is now integrated into your existing website! Users can click the chat button to open the widget and interact with your AI assistant.

Need help? Check that:
1. ✅ Your Render.com chatbot is running
2. ✅ The iframe URL matches your deployed service
3. ✅ All CSS, HTML, and JavaScript are properly added
4. ✅ No browser console errors
