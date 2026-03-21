import os
from groq import Groq
import google.generativeai as genai
from app.config import settings

class ChatService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        if not self.api_key:
            print("Warning: GROQ_API_KEY not found in settings. Attempting to read from environment variable.")
            # Fallback to os.getenv if not in settings for some reason
            self.api_key = os.getenv("GROQ_API_KEY_1")
        
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None
            
        self.model = "llama-3.3-70b-versatile"

    async def generate_response(self, prompt: str, model: str = "Groq Llama 3", system_prompt: str = "You are a helpful AI assistant."):
        if model == "Gemini Pro":
            print("Using Gemini Pro for response generation.")
            if not settings.GEMINI_API_KEY:
                return "Error: Gemini API key not configured."
            
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model_gemini = genai.GenerativeModel('gemini-2.5-flash')
                response = model_gemini.generate_content(f"{system_prompt}\n\n{prompt}")
                return response.text
            except Exception as e:
                return f"Error (Gemini): {str(e)}"

        if not self.client:
            return "Error: Groq API key not configured."

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.5,
                max_tokens=2048,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error (Groq): {str(e)}"
