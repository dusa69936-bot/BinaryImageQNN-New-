import re

canvas_path = r"c:\Users\91817\OneDrive\Documents\Desktop\BinaryImageQNN\assets\templates\users\UserHomeCanvas.html"
results_path = r"c:\Users\91817\OneDrive\Documents\Desktop\BinaryImageQNN\assets\templates\users\qnn_results.html"

new_bg_css = """body {
    background-color: #0f172a !important;
    background-image: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.92)), url("/static/img/custom_digits_bg.png") !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
}"""

with open(canvas_path, "r", encoding="utf-8") as f:
    canvas_text = f.read()

# Replace the body style we injected recently
canvas_text = re.sub(r'body\s*{[^}]*radial-gradient[^}]*}', new_bg_css, canvas_text)
# Optional fallback if it wasn't matched
if new_bg_css not in canvas_text:
    canvas_text = canvas_text.replace('<style>', f'<style>\n{new_bg_css}\n')

with open(canvas_path, "w", encoding="utf-8") as f:
    f.write(canvas_text)


with open(results_path, "r", encoding="utf-8") as f:
    results_text = f.read()

# Replace the body style in results path
results_text = re.sub(r'body\s*{[^}]*radial-gradient[^}]*}', new_bg_css + "\nbody { color: #f8fafc; overflow-x: hidden; }", results_text)

with open(results_path, "w", encoding="utf-8") as f:
    f.write(results_text)

print("Background Images Updated successfully.")
