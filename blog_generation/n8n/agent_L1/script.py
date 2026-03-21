import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env (3 levels up)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".env"))

import conditional_logic_prompt
import extract_links_prompt
import audience_specification_prompt
import eg_and_ref_prompt
import error_handling_prompt
import generate_topic_code_prompt

api_key = os.getenv("GROQ_API_KEY_1")
client = Groq(api_key=api_key)

MODEL = "llama-3.3-70b-versatile"

# Mapping of output files to their respective prompt logic
prompts_map = {
    "conditional_logic.txt": conditional_logic_prompt.PROMPT_LOGIC,
    "extract_links.txt": extract_links_prompt.PROMPT_LOGIC,
    "audience_specification.txt": audience_specification_prompt.PROMPT_LOGIC,
    "eg_and_ref.txt": eg_and_ref_prompt.PROMPT_LOGIC,
    "error_handling.txt": error_handling_prompt.PROMPT_LOGIC,
    "generate_topic_code.txt": generate_topic_code_prompt.PROMPT_LOGIC
}

# The order in which files should be merged (as per merge.py)
merge_order = [
    "conditional_logic.txt",
    "extract_links.txt",
    "audience_specification.txt",
    "eg_and_ref.txt",
    "error_handling.txt",
    "generate_topic_code.txt"
]

def run_prompt(prompt, input_text):
    """Executes a single prompt using the Groq API."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during API call: {str(e)}"

def main():
    # 1. Read input text
    input_file = "input.txt"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Reading input from {input_file}...")
    with open(input_file, "r", encoding="utf-8") as f:
        user_input = f.read()

    # 2. Run all prompts
    for filename in merge_order:
        print(f"Running prompt for: {filename}...")
        prompt_logic = prompts_map.get(filename)
        if prompt_logic:
            result = run_prompt(prompt_logic, user_input)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"Saved to {filename}")
        else:
            print(f"Warning: No prompt logic found for {filename}")

    # 3. Merge all outputs
    print("\nMerging files into merged_output.txt...")
    merged_content = ""
    for file in merge_order:
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                merged_content += f"\n===== {file} =====\n"
                merged_content += f.read() + "\n"
        else:
            print(f"Warning: Missing file {file}, skipping in merge.")

    # 4. Save final output
    with open("merged_output.txt", "w", encoding="utf-8") as f:
        f.write(merged_content)

    print("\nProcess complete! Final output is in 'merged_output.txt'.")
    print(merged_content[:500] + "..." if len(merged_content) > 500 else merged_content)

if __name__ == "__main__":
    main()
