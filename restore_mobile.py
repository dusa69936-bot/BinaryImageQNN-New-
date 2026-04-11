import re

file_path = r"c:\Users\91817\OneDrive\Documents\Desktop\BinaryImageQNN\assets\templates\users\qnn_results.html"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

mobile_preview_html = """
            <!-- Mobile Preview -->
            <div class="widget">
                <div class="widget-title">
                    Mobile Preview <i class="fa-solid fa-mobile-screen"></i>
                    <div class="badge" style="background:rgba(59,130,246,0.2); color:#93c5fd; border:1px solid #3b82f6;"><i class="fa-solid fa-eye"></i> Online</div>
                </div>
                <div class="upload-zone" style="margin-top: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 10px; cursor: pointer; padding: 25px; border-color: rgba(59,130,246,0.4);" onclick="openModal('mod-mobile')">
                    <div style="position: relative; font-size: 3.5rem; color: #3b82f6;">
                        <i class="fa-solid fa-mobile-screen"></i>
                        <i class="fa-solid fa-qrcode" style="position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); font-size: 1.5rem; color: #fff;"></i>
                    </div>
                    <div style="font-size: 1.1rem; color: #e2e8f0; font-weight: 600;">Open Mobile Scanner <i class="fa-solid fa-up-right-from-square" style="color: #60a5fa; font-size: 0.9rem; margin-left: 5px;"></i></div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Click to reveal QR Code & Controls</div>
                </div>
            </div>"""

# Find prediction history widget closure to inject after it
pattern = re.compile(r'(<div class="widget-title">Prediction History[\s\S]*?</div>\s*</div>\s*</div>)')

if "Mobile Preview" not in text:
    text = pattern.sub(r'\1' + mobile_preview_html, text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Mobile Preview restored successfully.")
else:
    print("Mobile Preview already exists.")
