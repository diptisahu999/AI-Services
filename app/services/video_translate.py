import os
import io
import re
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types as genai_types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extract_video_id(url):
    patterns = [r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("❌ Invalid YouTube URL")

def fetch_transcript_logic(video_url):
    """Extracts transcript from a YouTube video URL."""
    try:
        video_id = extract_video_id(video_url)
        # Fetch transcript using the new API version (1.2.4+)
        transcript = YouTubeTranscriptApi().fetch(video_id)

        # Format transcript text
        output = io.StringIO()
        for entry in transcript:
            output.write(f"{entry.start:.2f}s: {entry.text}\n")
        
        return True, output.getvalue()
    except Exception as e:
        return False, str(e)

def translate_transcript(transcript_text, target_language="Hindi"):
    """Translates the transcript text with automatic key rotation for quota limits."""
    keys = ["GEMINI_API_KEY_1", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3"]
    last_error = ""

    for key_name in keys:
        api_key = os.getenv(key_name)
        if not api_key:
            continue

        try:
            client = genai.Client(api_key=api_key)
            system_prompt = f"You are a professional translator. Translate the following video transcript into {target_language}. Keep the timestamps (e.g., 0.00s:) exactly where they are. Output only the translated text."
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=transcript_text,
                config=genai_types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3
                )
            )
            return True, response.text
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print(f"⚠️ Key {key_name} exhausted. Trying next key...")
                last_error = error_msg
                continue
            else:
                return False, f"Translation error: {error_msg}"

    return False, f"All API keys exhausted or failed. Last error: {last_error}"
