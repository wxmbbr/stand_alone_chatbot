#!/usr/bin/env python3
"""
BBR Network Chatbot Simple Launcher
Simplified script to start the Streamlit application
"""

import subprocess
import sys
import os
import time

def main():
    print("BBR Network Chatbot Simple Launcher")
    print("=" * 40)
    
    # Determine which app file to use
    app_files = [
        "app_streamlit_v2.py",  # Main version with scrolling fixes
        "app_streamlit.py"
    ]
    
    app_file = None
    for file in app_files:
        if os.path.exists(file):
            app_file = file
            break
    
    if not app_file:
        print("Error: No Streamlit app file found!")
        print("Expected files:", ", ".join(app_files))
        return
    
    print(f"Using app file: {app_file}")
    
    # Ask user what they want to run
    print("\nChoose an option:")
    print("1. Just run the chatbot (Streamlit only) - RECOMMENDED for testing scrolling")
    print("2. Run full web interface (Streamlit + HTTP server)")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        # Just run Streamlit
        print(f"\nStarting Streamlit chatbot ({app_file})...")
        print("The chatbot will be available at: http://localhost:8501")
        print("\nPress Ctrl+C to stop the server")
        print("\nNOTE: This version includes aggressive scrolling fixes!")
        print("You should now see a vertical scrollbar in the chat area.")
        
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", app_file, "--server.port=8501"], check=True)
        except KeyboardInterrupt:
            print("\nStopping chatbot...")
        except subprocess.CalledProcessError as e:
            print(f"Error running Streamlit: {e}")
    
    elif choice == "2":
        # Run both Streamlit and HTTP server
        print(f"\nStarting full web interface...")
        print("1. Starting Streamlit chatbot...")
        
        try:
            # Start Streamlit in background
            streamlit_process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", app_file, "--server.port=8501"
            ])
            
            print("Streamlit started on port 8501")
            
            # Wait a moment for Streamlit to start
            time.sleep(3)
            
            # Start HTTP server for the website
            print("2. Starting HTTP server for website...")
            print("Website will be available at: http://localhost:8000")
            print("Chatbot will be available at: http://localhost:8501")
            print("\nPress Ctrl+C to stop both servers")
            
            http_process = subprocess.Popen([
                sys.executable, "-m", "http.server", "8000"
            ])
            
            # Wait for user to stop
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping servers...")
                streamlit_process.terminate()
                http_process.terminate()
                print("Servers stopped.")
                
        except Exception as e:
            print(f"Error starting servers: {e}")
    
    else:
        print("Invalid choice. Please run the script again and choose 1 or 2.")

if __name__ == "__main__":
    main() 