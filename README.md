# Polynomial Examples Generator

A Streamlit app that generates real-world examples for polynomial functions, with graphing and analysis.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Add your OpenAI API key to `.streamlit/secrets.toml`:
   ```
   [groq]
   api_key = "your-api-key-here"
   ```
3. Run the app: `streamlit run app.py`

## Features

- Select polynomial degree and context
- Generate random polynomials
- Factor and analyze zeros/multiplicities
- Plot graphs
- AI-generated real-world examples