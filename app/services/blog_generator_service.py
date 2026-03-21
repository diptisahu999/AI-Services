import os
import json
import sys
import subprocess
import requests
import markdown
from dotenv import load_dotenv
from google import genai
from google.genai import types as genai_types
from pathlib import Path

# Load environment variables
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

# Setup Gemini SDK
api_keys = [os.getenv("GEMINI_API_KEY_1"), os.getenv("GEMINI_API_KEY_2"), os.getenv("GEMINI_API_KEY_3")]
api_keys = [k for k in api_keys if k]
current_key_index = 0

if api_keys:
    client = genai.Client(api_key=api_keys[current_key_index])
else:
    client = None

MODEL = "gemini-2.5-flash"

def run_prompt(system_prompt: str, user_content: str) -> str:
    """Executes a prompt with rotation support."""
    global client, current_key_index
    if not client:
        return "Error: No Gemini API keys configured."

    attempts = 0
    while attempts < len(api_keys):
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
            error_str = str(e).upper()
            if ("429" in error_str or "QUOTA" in error_str or "EXHAUSTED" in error_str) and (current_key_index + 1 < len(api_keys)):
                current_key_index += 1
                client = genai.Client(api_key=api_keys[current_key_index])
                attempts += 1
                continue
            return f"Error during Gemini API call: {str(e)}"
    return "Error: All Gemini API keys exhausted."

def format_to_text(data, indent=0):
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

async def generate_blog_from_video(video_url: str):
    """
    Complete orchestrated pipeline to generate a blog from a video URL.
    Returns: (success: bool, result: str) where result is HTML content or error.
    """
    # 1. Fetch Transcript
    try:
        api_url = "https://testscraper.techvizor.in/get_transcript"
        response = requests.post(api_url, data={"video_url": video_url})
        if response.status_code != 200:
            return False, f"Failed to fetch transcript: {response.text}"
        transcript = response.text
    except Exception as e:
        return False, f"Error fetching transcript: {str(e)}"

    # 2. Setup Prompt Imports (reusing the existing prompt logic)
    # We'll use absolute paths to import the prompt logic from the blog_generation directory
    BLOG_GEN_DIR = BASE_DIR / "blog_generation" / "n8n"
    sys.path.append(str(BLOG_GEN_DIR / "agent_L1"))
    sys.path.append(str(BLOG_GEN_DIR / "agent_L2"))
    sys.path.append(str(BLOG_GEN_DIR / "L3"))
    sys.path.append(str(BLOG_GEN_DIR / "L4"))

    try:
        import conditional_logic_prompt as l1_cond
        import extract_links_prompt as l1_links
        import audience_specification_prompt as l1_audience
        import eg_and_ref_prompt as l1_eg
        import error_handling_prompt as l1_err
        import generate_topic_code_prompt as l1_topic
        
        import generate_intro as l2_intro
        import refine_intro as l2_refine
        import step_guide_prompt as l2_step
        import customisation_prompt as l2_custom
        import issue_and_troubleshooting_prompt as l2_trouble
        import conclusion_prompt as l2_conc
        import CTA_prompt as l2_cta
        
        import cta_and_brand_prompt as l3_brand
        import generate_blog_prompt as l4_blog
    except ImportError as e:
        return False, f"System Error: Missing prompt logic modules. {str(e)}"

    # --- PHASE 1: L1 ---
    l1_outputs = {}
    l1_prompts = {
        "cond": l1_cond.PROMPT_LOGIC,
        "links": l1_links.PROMPT_LOGIC,
        "audience": l1_audience.PROMPT_LOGIC,
        "eg": l1_eg.PROMPT_LOGIC,
        "err": l1_err.PROMPT_LOGIC,
        "topic": l1_topic.PROMPT_LOGIC
    }
    
    # We only really need a subset for the next stage based on full_process.py
    l1_merged = ""
    for key, prompt in l1_prompts.items():
        raw = run_prompt(prompt, transcript)
        try:
            clean = raw.strip().replace("```json", "").replace("```", "").strip()
            data = json.loads(clean)
            formatted = format_to_text(data)
            l1_outputs[key] = formatted
        except:
            l1_outputs[key] = raw
            
    l1_merged = (
        f"Conditional_Logic\n{l1_outputs['cond']}\n"
        f"Audience_Specification\n{l1_outputs['audience']}\n"
        f"Example_and_References\n{l1_outputs['eg']}\n"
        f"Error_Handling\n{l1_outputs['err']}\n"
        f"Topic_and_Keywords\n{l1_outputs['topic']}\n"
        f"Video_Transcript: {transcript}\n"
    )

    # --- PHASE 2: L2 ---
    l2_outputs = {}
    l2_prompts = {
        "intro": l2_intro.PROMPT_LOGIC,
        "step": l2_step.PROMPT_LOGIC,
        "custom": l2_custom.PROMPT_LOGIC,
        "trouble": l2_trouble.PROMPT_LOGIC,
        "conc": l2_conc.PROMPT_LOGIC,
        "cta": l2_cta.PROMPT_LOGIC
    }
    for key, prompt in l2_prompts.items():
        l2_outputs[key] = run_prompt(prompt, l1_merged)

    blog_content = (
        f"Blog_Content\n"
        f"Introduction: {l2_outputs['intro']}\n"
        f"Step_By_Step_Guide: {l2_outputs['step']}\n"
        f"Customisation_Tips: {l2_outputs['custom']}\n"
        f"Issues_and_Troubleshooting: {l2_outputs['trouble']}\n"
        f"Conclusion: {l2_outputs['conc']}\n"
        f"Call-to-Action: {l2_outputs['cta']}"
    )

    # --- PHASE 3: L3 ---
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
    l4_input = (
        f"{blog_content}\n"
        f"Tutorial_Summary\n{l3_formatted['tutorial_summary']}\n"
        f"Company_Overview\n{l3_formatted['company_overview']}\n"
        f"CompanyURL\n{company_url}"
    )
    final_markdown = run_prompt(l4_blog.PROMPT_LOGIC, l4_input)
    
    # --- CONVERT TO HTML ---
    final_html = markdown.markdown(final_markdown)
    
    return True, final_html
