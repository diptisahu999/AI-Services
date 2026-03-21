import os
import json
import sys
import subprocess

# Auto-install missing packages into whichever Python is running this script
def _ensure_package(import_name, pip_name=None):
    try:
        __import__(import_name)
    except ImportError:
        pkg = pip_name or import_name
        print(f"Installing missing package: {pkg} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])

_ensure_package("dotenv", "python-dotenv")
_ensure_package("google.genai", "google-genai")
_ensure_package("markdown")
_ensure_package("requests")

from dotenv import load_dotenv
import markdown
import requests
from google import genai
from google.genai import types as genai_types

# Load environment variables from .env (located 2 levels up from this file)
load_dotenv(dotenv_path=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env"
))

# 1. SETUP GEMINI API (with rotation support)
api_keys = [os.getenv("GEMINI_API_KEY_1"), os.getenv("GEMINI_API_KEY_2"), os.getenv("GEMINI_API_KEY_3")]
api_keys = [k for k in api_keys if k] # Filter out empty keys

if not api_keys:
    raise ValueError("No Gemini API keys found in .env (GEMINI_API_KEY_1 or GEMINI_API_KEY_2).")

current_key_index = 0
client = genai.Client(api_key=api_keys[current_key_index])
MODEL = "gemini-2.5-flash"

# 2. HELPER FUNCTIONS
def run_prompt(system_prompt, user_content):
    """Executes a single prompt using the Google Gemini API with automatic key rotation."""
    global client, current_key_index
    
    while current_key_index < len(api_keys):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=user_content,
                config=genai_types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3
                )
            )
            return response.text
        except Exception as e:
            # Check for quota or rate limit errors
            error_str = str(e).upper()
            if ("429" in error_str or "QUOTA" in error_str or "EXHAUSTED" in error_str) and (current_key_index + 1 < len(api_keys)):
                current_key_index += 1
                print(f"⚠️ Rate limit or quota reached. Switching to Gemini API Key {current_key_index + 1}...")
                client = genai.Client(api_key=api_keys[current_key_index])
                continue
            return f"Error during Gemini API call: {str(e)}"
            
    return "Error: All Gemini API keys exhausted or failed."

def format_to_text(data, indent=0):
    """Converts a JSON-like object into the custom text format seen in the input files."""
    output = ""
    prefix = "  " * indent
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                output += f"{prefix}{k}\n{format_to_text(v, indent + 1)}"
            else:
                output += f"{prefix}{k}:{v}\n"
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, (dict, list)):
                output += f"{prefix}{i}\n{format_to_text(item, indent + 1)}"
            else:
                output += f"{prefix}{i}:{item}\n"
    else:
        output += f"{prefix}{data}\n"
    return output

def add_to_sys_path(path):
    if path not in sys.path:
        sys.path.append(path)

def main():
    # SETUP PATHS
    base_dir = r"f:\Ranjan\Demo-Project-Personal\ai_service_fastapi\blog_generation\n8n"
    l1_dir = os.path.join(base_dir, "agent_L1")
    l2_dir = os.path.join(base_dir, "agent_L2")
    l3_dir = os.path.join(base_dir, "L3")
    l4_dir = os.path.join(base_dir, "L4")

    # --- NEW PHASE: TRANSCRIPT SCRAPING ---
    print("\n--- PHASE 0: Fetching Transcript ---")
    video_url = input("Enter Video URL: ").strip()
    if not video_url:
        print("No URL provided. Expecting transcript to exist in 'agent_L1/input.txt'.")
    else:
        print(f"Fetching transcript for: {video_url}...")
        try:
            # 🔄 Use local logic instead of external API
            root_dir = os.path.dirname(os.path.dirname(base_dir))
            if root_dir not in sys.path:
                sys.path.append(root_dir)
            
            from video_translate import fetch_transcript
            transcript_text = fetch_transcript(video_url)
            
            if not transcript_text.startswith("Error:"):
                input_file = os.path.join(l1_dir, "input.txt")
                with open(input_file, "w", encoding="utf-8") as f:
                    f.write(transcript_text)
                print(f"✅ Transcript saved to '{input_file}'")
            else:
                print(f"❌ Failed to fetch transcript: {transcript_text}")
        except Exception as e:
            print(f"❌ Error during transcript scraping: {str(e)}")

    # --- PHASE 1: AGENT L1 ---
    print("\n--- PHASE 1: Running Agent L1 ---")
    add_to_sys_path(l1_dir)
    import conditional_logic_prompt as l1_cond
    import extract_links_prompt as l1_links
    import audience_specification_prompt as l1_audience
    import eg_and_ref_prompt as l1_eg
    import error_handling_prompt as l1_err
    import generate_topic_code_prompt as l1_topic

    # Read input transcript
    input_file = os.path.join(l1_dir, "input.txt")
    with open(input_file, "r", encoding="utf-8") as f:
        transcript = f.read()

    l1_outputs = {}
    l1_prompts = {
        "conditional_logic.txt": l1_cond.PROMPT_LOGIC,
        "extract_links.txt": l1_links.PROMPT_LOGIC,
        "audience_specification.txt": l1_audience.PROMPT_LOGIC,
        "eg_and_ref.txt": l1_eg.PROMPT_LOGIC,
        "error_handling.txt": l1_err.PROMPT_LOGIC,
        "generate_topic_code.txt": l1_topic.PROMPT_LOGIC
    }

    for filename, prompt in l1_prompts.items():
        print(f"Running L1 Prompt: {filename}")
        raw_output = run_prompt(prompt, transcript)
        
        # Try to parse JSON and format as structured text
        try:
            # Clean up potential markdown fences in JSON
            clean_json = raw_output.strip().replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            l1_outputs[filename] = format_to_text(data)
        except:
            l1_outputs[filename] = raw_output

        with open(os.path.join(l1_dir, filename), "w", encoding="utf-8") as f:
            f.write(l1_outputs[filename])

    # Merge for L2 input
    l1_merged = ""
    l1_merge_order = [
        ("Conditional_Logic", "conditional_logic.txt"),
        ("Audience_Specification", "audience_specification.txt"),
        ("Example_and_References", "eg_and_ref.txt"),
        ("Error_Handling", "error_handling.txt"),
        ("Topic_and_Keywords", "generate_topic_code.txt")
    ]
    for key, filename in l1_merge_order:
        l1_merged += f"{key}\n{l1_outputs[filename]}\n"
    l1_merged += f"Video_Transcript: {transcript}\n"
    
    with open(os.path.join(l2_dir, "input.txt"), "w", encoding="utf-8") as f:
        f.write(l1_merged)

    # --- PHASE 2: AGENT L2 ---
    print("\n--- PHASE 2: Running Agent L2 ---")
    add_to_sys_path(l2_dir)
    import generate_intro as l2_intro
    import refine_intro as l2_refine
    import step_guide_prompt as l2_step
    import customisation_prompt as l2_custom
    import issue_and_troubleshooting_prompt as l2_trouble
    import conclusion_prompt as l2_conc
    import CTA_prompt as l2_cta

    l2_outputs = {}
    l2_prompts = {
        "generate_intro.txt": l2_intro.PROMPT_LOGIC,
        "refine_intro.txt": l2_refine.PROMPT_LOGIC,
        "step_guide.txt": l2_step.PROMPT_LOGIC,
        "customization_tips.txt": l2_custom.PROMPT_LOGIC,
        "issue_and_troubleshooting.txt": l2_trouble.PROMPT_LOGIC,
        "conclusion.txt": l2_conc.PROMPT_LOGIC,
        "CTA.txt": l2_cta.PROMPT_LOGIC
    }

    for filename, prompt in l2_prompts.items():
        print(f"Running L2 Prompt: {filename}")
        l2_outputs[filename] = run_prompt(prompt, l1_merged)
        with open(os.path.join(l2_dir, filename), "w", encoding="utf-8") as f:
            f.write(l2_outputs[filename])

    # Prepare Blog_Content by stripping common markers like headings if any
    blog_content = (
        f"Blog_Content\n"
        f"Introduction: {l2_outputs['generate_intro.txt']}\n"
        f"Step_By_Step_Guide: {l2_outputs['step_guide.txt']}\n"
        f"Customisation_Tips: {l2_outputs['customization_tips.txt']}\n"
        f"Issues_and_Troubleshooting: {l2_outputs['issue_and_troubleshooting.txt']}\n"
        f"Conclusion: {l2_outputs['conclusion.txt']}\n"
        f"Call-to-Action: {l2_outputs['CTA.txt']}"
    )

    # --- PHASE 3: L3 ---
    print("\n--- PHASE 3: Running L3 ---")
    add_to_sys_path(l3_dir)
    import cta_and_brand_prompt as l3_brand
    company_url = "https://roongtadevelopers.com/"
    l3_input = f"Video_Transcript: {transcript}\nCompanyURL: {company_url}"
    l3_output_raw = run_prompt(l3_brand.PROMPT_LOGIC, l3_input)
    
    l3_formatted = {"tutorial_summary": "", "company_overview": ""}
    try:
        clean_json = l3_output_raw.strip().replace("```json", "").replace("```", "").strip()
        l3_data = json.loads(clean_json)
        l3_formatted["tutorial_summary"] = format_to_text(l3_data.get("tutorial_summary", {}))
        l3_formatted["company_overview"] = format_to_text(l3_data.get("company_overview", {}))
    except:
        l3_formatted["tutorial_summary"] = l3_output_raw

    # --- PHASE 4: L4 ---
    print("\n--- PHASE 4: Running L4 ---")
    add_to_sys_path(l4_dir)
    import generate_blog_prompt as l4_blog
    
    l4_input = (
        f"{blog_content}\n"
        f"Tutorial_Summary\n{l3_formatted['tutorial_summary']}\n"
        f"Company_Overview\n{l3_formatted['company_overview']}\n"
        f"CompanyURL\n{company_url}"
    )
    
    with open(os.path.join(l4_dir, "input.txt"), "w", encoding="utf-8") as f:
        f.write(l4_input)

    print("Running L4 Prompt: Final Blog Generation")
    final_blog = run_prompt(l4_blog.PROMPT_LOGIC, l4_input)
    
    with open(os.path.join(l4_dir, "generate_blog.txt"), "w", encoding="utf-8") as f:
        f.write(final_blog)
    
    # Also save to current directory for easy access
    with open("generate_blog.txt", "w", encoding="utf-8") as f:
        f.write(final_blog)

    print("\nSUCCESS! Full process complete.")
    print("Final blog generated in 'generate_blog.txt'.")

    # --- HTML CONVERSION ---
    print("\nConverting blog to HTML...")
    try:
        # 📥 Read the generated text file
        with open("generate_blog.txt", "r", encoding="utf-8") as f:
            text = f.read()

        # 🔄 Convert to HTML
        html = markdown.markdown(text)

        # 💾 Save HTML file
        with open("output.html", "w", encoding="utf-8") as f:
            f.write(html)

        print("✅ Converted to HTML successfully!")
    except Exception as e:
        print(f"❌ Error during HTML conversion: {str(e)}")

if __name__ == "__main__":
    main()
