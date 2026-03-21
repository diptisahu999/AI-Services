import markdown

# 📥 Read your text file
with open("generate_blog.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 🔄 Convert to HTML
html = markdown.markdown(text)

# 💾 Save HTML file
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Converted to HTML successfully!")