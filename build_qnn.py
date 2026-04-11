import os

html_content = """{% extends 'base.html' %}
{% load static %}

{% block styles %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;500;700&display=swap');

    body {
        margin: 0; padding: 0;
        background-color: #0d0a14 !important; /* Very dark background */
        background-image: radial-gradient(circle at 50% 50%, rgba(20, 10, 40, 0.8) 0%, rgba(4, 2, 10, 1) 100%) !important;
        color: #e2e8f0;
        font-family: 'Inter', system-ui, sans-serif;
    }

    .top-nav {
        display: flex; justify-content: space-between; padding: 15px 30px;
        background: rgba(0,0,0,0.5); border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    .logo-text { font-family: 'Orbitron', sans-serif; font-size: 1.5rem; font-weight: bold; color: #a855f7; display:flex; align-items:center; gap:10px; }
    .nav-links { display: flex; gap: 20px; align-items: center; font-size: 0.9rem; color: #94a3b8; }
    .nav-links span:hover { color: #fff; cursor: pointer; }

    .warning-banner {
        background: rgba(245, 158, 11, 0.1); border: 1px solid #f59e0b; color: #facc15;
        text-align: center; padding: 10px; margin: 15px 30px; font-weight: bold; border-radius: 8px;
        cursor: pointer; transition: 0.3s;
    }
    .warning-banner:hover { background: rgba(245, 158, 11, 0.2); }

    .sci-fi-dashboard {
        padding: 10px 30px; max-width: 1900px; margin: 0 auto;
        display: grid; grid-template-columns: 1.1fr 1.3fr 1.3fr 1.1fr; gap: 20px;
    }

    .sci-box {
        background: rgba(20, 15, 35, 0.6); border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px; padding: 15px; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3); backdrop-filter: blur(10px);
    }

    .panel-label {
        font-family: 'Inter', sans-serif; font-size: 0.9rem; font-weight: 700; color: #f8fafc;
        display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px;
    }

    .transport-btn, .action-btn {
        background: linear-gradient(90deg, #8b5cf6, #3b82f6); border: none; border-radius: 8px;
        padding: 10px; width: 100%; color: white; font-weight: bold; cursor: pointer; transition: 0.3s;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    }
    .transport-btn:hover { background: linear-gradient(90deg, #7c3aed, #2563eb); }
    
    .action-btn { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); box-shadow: none; font-size: 0.8rem; }
    .action-btn:hover { background: rgba(139, 92, 246, 0.2); border-color: #a855f7; }

    .bar-wrap { background: rgba(0,0,0,0.5); height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 15px; width: 100%;}
    .bar-fill { height: 100%; border-radius: 4px; }
    
    .history-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; color: #f8fafc; }
    .history-table th { background: rgba(0,0,0,0.5); padding: 8px 5px; color: #10b981; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }
    .history-table td { padding: 10px 5px; border-bottom: 1px solid rgba(255,255,255,0.05); cursor:pointer; }
    .history-table tr:hover td { background: rgba(139, 92, 246, 0.1); }

    .acc-big { font-family: 'Orbitron', sans-serif; font-size: 3rem; color: #fff; text-align: center; margin-top: -60px; font-weight: bold; }
    .badge { background: rgba(59,130,246,0.2); color: #38bdf8; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; }

    .drag-drop-box { border: 2px dashed rgba(168, 85, 247, 0.4); border-radius: 8px; height: 120px; display: flex; align-items:center; justify-content:center; flex-direction:column; color: #94a3b8; margin-bottom: 15px;}
    .drag-drop-box i { font-size: 2rem; margin-bottom: 10px; color: #a855f7; }

</style>
{% endblock %}

{% block contents %}
<!-- Navigation Bar (30) -->
<div class="top-nav">
    <div class="logo-text"><i class="fa-solid fa-atom"></i> QuantumVision</div>
    <div class="nav-links">
        <span onclick="window.location.href='/'"><i class="fa-solid fa-house"></i> Home</span>
        <span>Dataset</span>
        <span>EDA</span>
        <span style="color:#fff; font-weight:bold; border-bottom: 2px solid #a855f7;">Accuracy</span>
        <span onclick="window.location.href='{% url 'UserTestCanvasMNIST' %}'">Canvas</span>
        <span>Logout <i class="fa-solid fa-ellipsis"></i></span>
    </div>
    <div class="nav-links">
        <span><i class="fa-solid fa-moon"></i> Dark Mode (28)</span>
        <span><i class="fa-solid fa-globe"></i> English (29)</span>
        <span class="badge">Version 2.1 <i class="fa-solid fa-rotate"></i></span>
    </div>
</div>

<!-- Warning Message (26) & Improvement Tips (19) -->
<div class="warning-banner" onclick="infoAlert('Retrain Model using the controls below!')">
    <i class="fa-solid fa-triangle-exclamation"></i> WARNING: Retrain recommended for better accuracy (Tip 19) <i class="fa-solid fa-circle-info"></i>
</div>

<div class="sci-fi-dashboard">

    <!-- COL 1 -->
    <div>
        <!-- 1, 2, 24. Upload & Drag Drop -->
        <div class="sci-box">
             <label class="panel-label">1. Upload Digit Images <i class="fa-solid fa-circle-info"></i></label>
             <div class="drag-drop-box" onclick="document.location.href='{% url 'UserTestCanvasMNIST' %}'">
                 <i class="fa-solid fa-cloud-arrow-up"></i>
                 <span>2. Drag and Drop to add images</span>
             </div>
             <button class="transport-btn" onclick="document.location.href='{% url 'UserTestCanvasMNIST' %}'">24. Transport / Upload Image</button>
        </div>
        
        <!-- 3, 4. Augmentation Preview -->
        <div class="sci-box">
             <label class="panel-label">3. Augmentation Preview <i class="fa-solid fa-layer-group"></i></label>
             <div style="display:flex; justify-content:space-between; margin-bottom:15px; color:#a855f7; font-size:1.2rem;">
                 <i class="fa-solid fa-crop-simple"></i><i class="fa-solid fa-droplet"></i><i class="fa-solid fa-wand-magic-sparkles"></i><i class="fa-solid fa-image"></i>
             </div>
             <button class="action-btn" onclick="infoAlert('Integrating models...')"><i class="fa-solid fa-link"></i> 4. Integrate Preview Model</button>
        </div>
        
        <!-- 5, 6, 7. Quick Retrain / Top-5 -->
        <div class="sci-box">
             <label class="panel-label">5. Quick Retrain Model <i class="fa-solid fa-bolt"></i></label>
             <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:10px;">
                 <span>6. Learning Rate</span><span style="color:#10b981;">0.001 <i class="fa-solid fa-chevron-down"></i></span>
             </div>
             <div class="action-btn" style="margin-bottom:10px; display:flex; justify-content:space-between;">
                 <span>7. Top-5 Predictions</span> <span>97% <i class="fa-solid fa-caret-down"></i></span>
             </div>
             <div class="action-btn" style="display:flex; justify-content:space-between;">
                 <span>7. Top-1 Predictions</span> <span>92% <i class="fa-solid fa-caret-down"></i></span>
             </div>
        </div>

        <!-- 8, 27. Model Save & Load, Sound Control -->
        <div class="sci-box" style="display:flex; justify-content:space-between; align-items:center;">
             <span style="font-size:0.9rem; font-weight:bold;"><i class="fa-solid fa-microchip"></i> 8. Model Save & Load</span>
             <i class="fa-solid fa-circle-xmark" style="color:#ef4444;"></i>
        </div>
        <div class="sci-box" style="display:flex; align-items:center; gap:10px; cursor:pointer;" onclick="infoAlert('Sound Toggled')">
             <i class="fa-solid fa-volume-high" style="color:#a855f7;"></i> <span style="font-weight:bold;">27. Sound ON</span>
        </div>
    </div>
    
    <!-- COL 2 -->
    <div>
        <!-- 9, 10. Live Accuracy (Big) -->
        <div class="sci-box">
             <label class="panel-label"><span style="color:#38bdf8;">9. Live Accuracy</span> <span class="badge" style="cursor:pointer;" onclick="location.reload()">10. Refresh <i class="fa-solid fa-rotate-right"></i></span></label>
             <div style="height: 140px; position: relative;"><canvas id="gaugeBig"></canvas></div>
             <div class="acc-big" id="ui-acc-val1">99.40%</div>
             <div style="text-align:center; font-size:0.8rem; color:#64748b; margin-top:5px;">Recent Batches: 302 / 405</div>
        </div>
        
        <!-- 11, 12. Real-Time Logs & Progress -->
        <div class="sci-box">
             <label class="panel-label"><span style="color:#10b981;">11. Real-Time Logs</span> <span style="font-size:0.8rem;"><i class="fa-solid fa-spinner fa-spin"></i> 12. Progress</span></label>
             <div style="font-size:0.75rem; color:#94a3b8; margin-bottom:5px; display:flex; justify-content:space-between;"><span>Epoch Iterations</span> <span>85.0%</span></div>
             <div class="bar-wrap"><div class="bar-fill" style="width:85%; background: linear-gradient(90deg, #ef4444, #f59e0b);"></div></div>
             <div style="font-size:0.75rem; color:#94a3b8; margin-bottom:5px; display:flex; justify-content:space-between;"><span>Batch Sync</span> <span>51.7%</span></div>
             <div class="bar-wrap"><div class="bar-fill" style="width:51.7%; background: linear-gradient(90deg, #3b82f6, #8b5cf6);"></div></div>
             <p style="font-size:0.7rem; color:#64748b; margin:0;">System extrapolating tensor metrics continuously...</p>
        </div>
        
        <!-- 14. Dataset Info -->
        <div class="sci-box">
             <label class="panel-label">14. Dataset Info <i class="fa-solid fa-database"></i></label>
             <div style="text-align:center; font-size:0.9rem; font-weight:bold; margin-bottom:15px;">Training Count : 58,420 (Even & Odd)</div>
             <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-bottom:5px;"><span>Augmented: 21,220 (36%)</span> <span>Rest: 37,200 (64%)</span></div>
             <div class="bar-wrap" style="height:12px; display:flex;"><div style="width:36%; background:#10b981;"></div><div style="width:64%; background:#ef4444;"></div></div>
        </div>
        
        <!-- 15, 16, 17, 18. Model Performance & XAI Heatmap & Cloud Storage -->
        <div class="sci-box">
             <label class="panel-label">15. Model Performance (16. XAI Heatmap)</label>
             <div style="display:flex; gap:15px; margin-bottom:15px;">
                 <div style="flex:1; background:#000; border-radius:8px; display:flex; align-items:center; justify-content:center; overflow:hidden;">
                     <img src="https://upload.wikimedia.org/wikipedia/commons/2/27/MnistExamples.png" style="width:100%; opacity:0.7; filter: hue-rotate(90deg) contrast(200%);" alt="heatmap">
                 </div>
                 <div style="flex:1; font-size:0.75rem; color:#94a3b8;">
                     <div style="margin-bottom:10px;"><i class="fa-solid fa-clock text-blue"></i> Latency: <b>50 ms</b></div>
                     <div><i class="fa-solid fa-wave-square text-orange"></i> L-Rate: 0.0011v</div>
                 </div>
             </div>
             <div style="display:flex; gap:10px;">
                 <button class="action-btn" style="flex:1;"><i class="fa-solid fa-download"></i> 17. Load Model</button>
                 <button class="action-btn" style="flex:1; border-color:#38bdf8;" onclick="infoAlert('Syncing to Cloud...')"><i class="fa-solid fa-cloud"></i> 18. Cloud Storage</button>
             </div>
        </div>
    </div>
    
    <!-- COL 3 -->
    <div>
        <!-- 13, 25. Model Version & Compare Feed -->
        <div class="sci-box">
             <label class="panel-label">13. Model Version v2.1.0 <span style="font-size:0.7rem; font-weight:normal; cursor:pointer;"><i class="fa-solid fa-code-compare"></i> 25. Compare Models</span></label>
             <div style="display:flex; gap:10px; margin-bottom:15px;">
                 <span class="badge" style="background:rgba(168,85,247,0.2) !important; color:#a855f7;">+ Quantum N.N.</span>
                 <span class="badge" style="background:rgba(255,255,255,0.1); color:#fff;">v1.0 CNN</span>
                 <span class="badge" style="background:rgba(16,185,129,0.2); color:#10b981;">v2.0 QNN</span>
             </div>
             <div style="font-size:0.75rem; color:#94a3b8; line-height:1.8;">
                 <div><i class="fa-solid fa-check-circle" style="color:#10b981;"></i> 17:05:25 - Format optimized. Augmentation classes.</div>
                 <div><i class="fa-solid fa-circle-xmark" style="color:#facc15;"></i> 17:03:59 - Beta image (uploaded wrong format).</div>
                 <div><i class="fa-solid fa-triangle-exclamation" style="color:#ef4444;"></i> 16:35:29 - Prediction False: Expected 7.</div>
             </div>
        </div>
        
        <!-- Model Version Graph -->
        <div class="sci-box">
             <label class="panel-label"><i class="fa-solid fa-chart-simple"></i> Model Version Analytics</label>
             <div style="height: 120px; position:relative;"><canvas id="versionBarChart"></canvas></div>
        </div>

        <!-- 20. Dataset Distribution -->
        <div class="sci-box">
             <label class="panel-label">20. Dataset Distribution <i class="fa-solid fa-chart-pie"></i></label>
             <table class="history-table">
                 <tr><th>Digit</th><th>Samples</th><th>Ratio</th></tr>
                 <tr><td>0, 1, 2</td><td>~6,000 ea</td><td><span style="color:#10b981;">30%</span></td></tr>
                 <tr><td>3, 4, 5</td><td>~5,500 ea</td><td><span style="color:#38bdf8;">28%</span></td></tr>
                 <tr><td>6, 7, 8, 9</td><td>~5,800 ea</td><td><span style="color:#f59e0b;">42%</span></td></tr>
             </table>
        </div>
    </div>

    <!-- COL 4 -->
    <div>
        <!-- Live Accuracy (Small view as per image) -->
        <div class="sci-box">
             <label class="panel-label">Live Accuracy (Local)</label>
             <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                 <span style="font-size:2rem; font-family:'Orbitron', sans-serif; font-weight:bold; color:#10b981;" id="ui-acc-val2">99.40%</span>
                 <span style="font-size:0.8rem; color:#94a3b8;">Based on recent preds</span>
             </div>
             <div style="height: 60px; position: relative;"><canvas id="miniGauge"></canvas></div>
        </div>
        
        <!-- Real-Time Logs Small List -->
        <div class="sci-box">
             <label class="panel-label">Real-Time Logs <i class="fa-solid fa-terminal"></i></label>
             <div style="font-size:0.75rem; color:#94a3b8; line-height:1.8;">
                 <div>> Epoch tracking initiated...</div>
                 <div>> <span style="color:#ef4444;">Prediction False (8->3)</span> via Loss Curve</div>
                 <div>> Restoring state metrics... API Synced.</div>
             </div>
        </div>
        
        <!-- 22, 23. Mobile Preview & API -->
        <div class="sci-box" style="text-align:center;">
             <label class="panel-label" style="justify-content:center;">23. Mobile Preview (<i class="fa-solid fa-network-wired"></i> 22. API Integration)</label>
             <div style="display:flex; align-items:center; justify-content:center; gap:15px; margin-top:10px;">
                 <div style="border:1px solid rgba(255,255,255,0.2); border-radius:12px; width:60px; height:100px; display:flex; align-items:center; justify-content:center; flex-direction:column; background:#000;">
                     <div style="width:40px; height:40px; background:linear-gradient(45deg, #8b5cf6, #3b82f6); border-radius:4px; margin-bottom:5px;"></div>
                     <div style="width:30px; height:2px; background:rgba(255,255,255,0.3);"></div>
                 </div>
                 <div style="width:80px; height:80px; background:#fff; padding:5px; border-radius:4px;">
                     <img src="https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_mobile_English_Wikipedia.svg" style="width:100%; height:100%;">
                 </div>
             </div>
             <div style="font-size:0.75rem; color:#94a3b8; margin-top:10px;">Scan to test API inference</div>
        </div>
        
        <!-- 21. Prediction History Table -->
        <div class="sci-box">
             <label class="panel-label">21. Prediction History</label>
             <table class="history-table" style="font-size:0.9rem;">
                 <thead><tr><th>Image</th><th>Predicted</th><th>Acc</th><th>Loss</th></tr></thead>
                 <tbody id="ui-history-list">
                     <!-- dynamically populated via JS -->
                     <tr><td colspan="4" style="text-align:center;">Waiting for data...</td></tr>
                 </tbody>
             </table>
        </div>
    </div>
</div>

{% endblock %}

{% block scripts %}
<script>
function infoAlert(msg) {
    Swal.fire({
        title: 'Quantum Dashboard Action', text: msg, icon: 'success', background: '#100c1c', color: '#f8fafc',
        toast: true, position: 'top-end', timer: 3000, showConfirmButton: false
    });
}

document.addEventListener('DOMContentLoaded', () => {

    const historyQueue = JSON.parse(localStorage.getItem('qnn_predictions_history')) || [];
    let displayAccuracy = "99.40"; 
    
    if(historyQueue.length > 0) {
        let latest = historyQueue[0];
        displayAccuracy = parseFloat(latest.liveAcc).toFixed(2);
        
        if (latest.image) {
            document.getElementById('base-uploaded-img') && (document.getElementById('base-uploaded-img').src = latest.image);
        }

        let hl = document.getElementById('ui-history-list');
        if(hl) {
            hl.innerHTML = '';
            historyQueue.slice(0, 5).forEach((item, idx) => {
                let clr = item.isCorrect ? '#10b981' : '#ef4444';
                let loss = (100 - item.accuracy).toFixed(2);
                hl.innerHTML += `<tr onclick="restoreToCanvas(${idx})">
                    <td><span style="color:#94a3b8;">${item.actual} <i class="fa-solid fa-angle-right"></i></span></td>
                    <td style="color:${clr}; font-weight:bold;">${item.prediction}</td>
                    <td style="color:#38bdf8;">${Math.round(item.accuracy)}%</td>
                    <td style="color:#f59e0b;">${loss}%</td>
                </tr>`;
            });
        }
    }

    document.getElementById('ui-acc-val1') && (document.getElementById('ui-acc-val1').innerText = displayAccuracy + "%");
    document.getElementById('ui-acc-val2') && (document.getElementById('ui-acc-val2').innerText = displayAccuracy + "%");

    Chart.defaults.color = 'rgba(255,255,255,0.4)';
    const noGridOpts = { 
        responsive: true, maintainAspectRatio: false, 
        plugins: { legend: {display: false}, tooltip: {enabled:false} }, 
        scales: { x: { display:false }, y: { display:false } },
        elements: { point: { radius: 0 } }
    };

    // Big Doughnut
    if(document.getElementById('gaugeBig')) {
        new Chart(document.getElementById('gaugeBig').getContext('2d'), {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [parseFloat(displayAccuracy), 100 - parseFloat(displayAccuracy)],
                    backgroundColor: ['#10b981', 'rgba(255,255,255,0.05)'],
                    borderWidth: 0, borderRadius: 10, cutout: '80%'
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, rotation: -90, circumference: 180,
                plugins: { tooltip: { enabled: false } }, animation: { animateRotate: true }
            }
        });
    }

    // Mini Gauge
    if(document.getElementById('miniGauge')) {
        new Chart(document.getElementById('miniGauge').getContext('2d'), {
            type: 'line',
            data: { labels: ['1','2','3','4','5'], datasets: [{ data: [70, 75, 80, 85, parseFloat(displayAccuracy)], borderColor: '#10b981', tension: 0.4 }] },
            options: noGridOpts
        });
    }

    // Version Bar Chart
    if(document.getElementById('versionBarChart')) {
        new Chart(document.getElementById('versionBarChart').getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Net 1', 'Net 2', 'Net 3', 'Net 4'],
                datasets: [
                    { data: [65, 80, 50, 95], backgroundColor: '#a855f7', borderRadius: 4 },
                    { data: [55, 75, 45, 90], backgroundColor: '#3b82f6', borderRadius: 4 }
                ]
            },
            options: { responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{x:{display:false},y:{display:false}} }
        });
    }
});

function restoreToCanvas(idx) {
    sessionStorage.setItem('restore_prediction', idx);
    window.location.href = "{% url 'UserTestCanvasMNIST' %}";
}

</script>
{% endblock %}
"""
with open(r'c:\Users\91817\OneDrive\Documents\Desktop\BinaryImageQNN\assets\templates\users\qnn_results.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print("File regenerated fully!")
