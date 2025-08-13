#!/usr/bin/env python3
"""
Cleanup script to remove unused files from the project.
This helps maintain a clean project structure with only the necessary files.
"""

import os
import shutil

# List of files to keep (essential files)
KEEP_FILES = [
    # Core application files
    "app_streamlit_v2.py",       # Recommended v2 API implementation
    "index.html",                # Web interface
    "config.py",                 # Configuration file
    "run.py",                    # Launcher script
    "requirements.txt",          # Dependencies
    "README.md",                 # Documentation
    ".env",                      # Optional environment variables
    ".gitignore",                # Git ignore file
    "cleanup.py",                # This script
    
    # Hidden directories (beginning with .)
    ".git",
    ".vscode",
    ".idea",
    
    # Virtual environment (if in the project directory)
    "venv",
    "venvope"
]

# Temporary files that shouldn't be committed but can be kept locally
TEMP_FILES = [
    "__pycache__",
    "*.pyc",
    ".DS_Store",
    "temp_openai_query.py"
]

# Files that can be safely deleted (will be prompted for confirmation)
UNUSED_FILES = [
    "app_streamlit.py",          # Original implementation with potential proxy issues
    "app_streamlit_fixed.py",    # Fixed implementation
    "app_streamlit_final.py",    # Final styling implementation
    "app_streamlit_robust.py",   # Robust subprocess implementation 
    "app_streamlit_direct.py",   # Direct API implementation
    "app_streamlit_proxy_fix.py", # Proxy fix implementation
    "test_openai.py",            # Test script for OpenAI API
    "test_openai_direct.py",     # Test script for direct HTTP requests
    "debug_openai.py"            # Debug script for OpenAI client
]

def should_keep(file_path):
    """Determine if a file should be kept based on the KEEP_FILES list."""
    
    # Check for exact filename matches
    if file_path in KEEP_FILES:
        return True
    
    # Check hidden directories
    if file_path.startswith('.') and os.path.isdir(file_path):
        return True
    
    # Check virtual environment directories
    if file_path.startswith('venv') and os.path.isdir(file_path):
        return True
    
    return False

def main():
    print("BBR Network OpenAI Assistant Chat - Cleanup Script")
    print("------------------------------------------------")
    print("This script will help you clean up unused files in the project.")
    print("The following files will be kept:")
    for file in KEEP_FILES:
        print(f"  - {file}")
    
    print("\nThe following files will be suggested for removal:")
    found_unused = []
    for file in UNUSED_FILES:
        if os.path.exists(file):
            found_unused.append(file)
            print(f"  - {file}")
    
    if not found_unused:
        print("  No unused files found to remove!")
        return
    
    confirm = input("\nDo you want to remove these files? (y/n): ")
    if confirm.lower() != 'y':
        print("Cleanup cancelled.")
        return
    
    # Remove unused files
    for file in found_unused:
        try:
            if os.path.isdir(file):
                shutil.rmtree(file)
            else:
                os.remove(file)
            print(f"Removed: {file}")
        except Exception as e:
            print(f"Error removing {file}: {str(e)}")
    
    print("\nCleanup completed!")

if __name__ == "__main__":
    main() 