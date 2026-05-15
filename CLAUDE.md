# CLAUDE.md — Instructions for Claude

## About the Developer
I am a mathematics educator with zero coding experience. I am a college algebra
instructor using AI tools to build educational apps for my own teaching practice.
Please explain all code suggestions clearly and in plain language. Assume I am
new to all programming concepts.

## Project Context
I created an app using copilot in VS code. It uses Ollama but it is very slow, not easy to share, and I have not figured out how to get all of the code to GitHub. I need to update the application so that it is in a cloud-based system that won't cost me anything to use, upload my code into by GitHub account, and share that application.

## Preferred Tools and Stack
- **Language:** Python
- **UI Framework:** Streamlit
- **AI Integration:** Groq API
- **Version Control:** GitHub
- **Editor:** VS Code

## How to Help Me
- Always explain what each piece of code does in plain English
- Keep code simple and beginner-friendly
- Walk me through tasks one step at a time and wait for confirmation
- When suggesting fixes, explain what was wrong and why the fix works
- Remind me to update requirements.txt when adding new libraries
- Remind me to add new API keys to both secrets.toml and Streamlit Cloud
- Remind me to push changes to GitHub after significant updates

## Project Structure
- App logic lives in app.py
- Dependencies are listed in req