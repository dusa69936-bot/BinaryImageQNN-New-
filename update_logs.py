import re

file_path = r"c:\Users\91817\OneDrive\Documents\Desktop\BinaryImageQNN\assets\templates\users\qnn_results.html"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Replace Real-Time Logs HTML
modal_logs_re = re.compile(r'<div style="display:flex; flex-direction:column; gap:15px; margin-top:20px;">\s*<div style="display:flex; justify-content:space-between; align-items:center; background:rgba\(255,255,255,0\.03\);[\s\S]*?</div>\s*</div>')

new_modal_html = '''<div id="dynamic-log-list" style="display:flex; flex-direction:column; gap:15px; margin-top:20px;">
                <!-- Dynamically populated via populateDashboard -->
            </div>'''
text = modal_logs_re.sub(new_modal_html, text)

# 2. Append Logic to populateDashboard
populate_logic_to_append = '''

    // Populate Real-Time Logs dynamically
    let logContainer = document.getElementById("dynamic-log-list");
    if (logContainer) {
        logContainer.innerHTML = "";
        
        // Let's display the top 3-4 latest predictions
        const latestEvents = historyQueue.slice(0, 4);
        latestEvents.forEach((ev, i) => {
            let statusIcon = ev.isCorrect ? '<div style="width:24px; height:24px; background:rgba(16,185,129,0.1); color:#10b981; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 0 10px #10b981;"><i class="fa-solid fa-check-double"></i></div>' : '<div style="width:24px; height:24px; background:rgba(239,68,68,0.1); color:#ef4444; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 0 10px #ef4444;"><i class="fa-solid fa-xmark"></i></div>';
            
            let msg = ev.isCorrect ? `Prediction True: Matched ${ev.actual}` : `Prediction False: Expected ${ev.actual}, Got ${ev.prediction}`;
            
            let color = ev.isCorrect ? '#10b981' : '#ef4444';
            
            let htmlLog = `<div style="display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.03); padding:10px; border-radius:8px; border:1px solid rgba(255,255,255,0.05);">
                <div style="display:flex; gap:10px; align-items:center; font-size:0.8rem; color:#cbd5e1; font-weight:500;">
                    ${statusIcon}
                    <span style="color:${color}">${msg}</span>
                </div>
                <span class="badge" style="background:rgba(255,255,255,0.1); font-size:0.7rem;">Exp ${ev.actual}</span>
            </div>`;
            logContainer.innerHTML += htmlLog;
        });
        
        // Add a general system info tag
        if(total > 0) {
           logContainer.innerHTML += `<div style="display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.03); padding:10px; border-radius:8px; border:1px solid rgba(255,255,255,0.05);">
                <div style="display:flex; gap:10px; align-items:center; font-size:0.8rem; color:#cbd5e1; font-weight:500;">
                    <div style="width:24px; height:24px; background:rgba(59,130,246,0.1); color:#3b82f6; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 0 10px #3b82f6;"><i class="fa-solid fa-server"></i></div>
                    Live System Active. Memory nominal.
                </div>
                <span class="badge" style="background:rgba(255,255,255,0.1); font-size:0.7rem;">OK</span>
            </div>`;
        }
    }
'''

# Find the end of populateDashboard function
text = text.replace("document.querySelectorAll(\"span\").forEach(el => {\n        if(el.innerText && el.innerText.includes(\" / \") && el.parentNode.style.position === \"absolute\") {\n            el.innerText = `${correct} / ${total}`;\n        }\n    });", 
'''document.querySelectorAll("span").forEach(el => {\n        if(el.innerText && el.innerText.includes(" / ") && el.parentNode.style.position === "absolute") {\n            el.innerText = `${correct} / ${total}`;\n        }\n    });''' + populate_logic_to_append)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Real-time Logs Update Complete")
