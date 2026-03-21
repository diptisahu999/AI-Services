import os

files = ["generate_intro.txt", "refine_intro.txt", "step_guide.txt", "customization_tips.txt", "issue_and_troubleshooting.txt", "conclusion.txt", "CTA.txt"]

merged_content = ""

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        merged_content += f"\n===== {file} =====\n"
        merged_content += f.read() + "\n"

# Save final output
with open("merged_output.txt", "w", encoding="utf-8") as f:
    f.write(merged_content)

print("✅ Files merged successfully!")