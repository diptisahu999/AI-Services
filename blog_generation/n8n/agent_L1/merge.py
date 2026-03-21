import os

files = ["conditional_logic.txt","extract_links.txt", "audience_specification.txt",  "eg_and_ref.txt", "error_handling.txt","generate_topic_code.txt"]

merged_content = ""

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        merged_content += f"\n===== {file} =====\n"
        merged_content += f.read() + "\n"

# Save final output
with open("merged_output.txt", "w", encoding="utf-8") as f:
    f.write(merged_content)

print("✅ Files merged successfully!")