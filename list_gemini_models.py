import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY_1')

if not api_key:
    print("API Key 1 not found")
else:
    try:
        genai.configure(api_key=api_key)
        print(f"Checking models for API key: {api_key[:10]}...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")
