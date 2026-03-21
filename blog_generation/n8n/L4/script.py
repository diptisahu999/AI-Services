import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env (3 levels up)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".env"))

api_key = os.getenv("GROQ_API_KEY_2")
from generate_blog_prompt import PROMPT_LOGIC


client = Groq(api_key=api_key)

MODEL = "llama-3.3-70b-versatile"


def run_prompt(input_text):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": PROMPT_LOGIC},
                {"role": "user", "content": input_text}
            ],
            temperature=0.3  # lower for structured output
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as f:
        user_input = f.read()

    result = run_prompt(user_input)

    print("\n🚀 OUTPUT: \n")
    with open("generate_blog.txt", "w", encoding="utf-8") as f:
        f.write(result)
    print(result)