import textwrap
content = """
    <div class="dashboard-grid">
        <!-- COLUMN 1: LEFT -->
        <div style="display: flex; flex-direction: column; gap: 1.2rem;">
            <!-- Upload Digit Images -->
            <div class="widget">
                <div class="widget-title">Upload Digit Images <i class="fa-solid fa-cloud-arrow-up"></i></div>
                <div class="upload-zone" style="margin-top: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 10px; cursor: pointer; padding: 25px; border-color: rgba(139,92,246,0.4);" onclick="document.getElementById('imgUpload').click()">
                    <div style="position: relative; font-size: 3.5rem; color: #8b5cf6;">
                        <i class="fa-solid fa-laptop-code"></i>
                        <i class="fa-solid fa-upload" style="position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); font-size: 1.5rem; color: #fff;"></i>
                    </div>
                    <div style="font-size: 1.1rem; color: #e2e8f0; font-weight: 600;">Open Image Uploader <i class="fa-solid fa-up-right-from-square" style="color: #60a5fa; font-size: 0.9rem; margin-left: 5px;"></i></div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Click to open direct file upload</div>
                </div>
                <input type="file" id="imgUpload" style="display:none;" onchange="handleUIUpload(event)">
            </div>
            
            <!-- Augmentation Preview -->
            <div class="widget">
                <div class="widget-title">Augmentation Preview <i class="fa-solid fa-layer-group"></i></div>
                <div class="upload-zone" style="margin-top: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 10px; cursor: pointer; padding: 25px; border-color: rgba(96,165,250,0.4);" onclick="openModal('mod-augment')">
                    <div style="position: relative; font-size: 3.5rem; color: #60a5fa;">
                        <i class="fa-solid fa-photo-film"></i>
                        <i class="fa-solid fa-wand-magic-sparkles" style="position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); font-size: 1.5rem; color: #fff;"></i>
                    </div>
                    <div style="font-size: 1.1rem; color: #e2e8f0; font-weight: 600;">Open Augmentation <i class="fa-solid fa-up-right-from-square" style="color: #60a5fa; font-size: 0.9rem; margin-left: 5px;"></i></div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Click to reveal Image Smart Tools</div>
                </div>
            </div>

            <!-- Quick Retrain Model & Predictions -->
            <div class="widget">
                <div class="widget-title">Quick Retrain Model <i class="fa-solid fa-bolt" style="color:#f59e0b;"></i></div>
                <div class="upload-zone" style="margin-top: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 10px; cursor: pointer; padding: 25px; border-color: rgba(245,158,11,0.4);" onclick="openModal('mod-retrain')">
                    <div style="position: relative; font-size: 3.5rem; color: #f59e0b;">
                        <i class="fa-solid fa-microchip"></i>
                        <i class="fa-solid fa-bolt" style="position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); font-size: 1.5rem; color: #fff;"></i>
                    </div>
                    <div style="font-size: 1.1rem; color: #e2e8f0; font-weight: 600;">Open QNN Retrain <i class="fa-solid fa-up-right-from-square" style="color: #60a5fa; font-size: 0.9rem; margin-left: 5px;"></i></div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Click to modify Hyperparameters</div>
                </div>
            </div>

            <!-- Explainable AI -->
            <div class="widget" style="flex:1;">
                <div class="widget-title">Explainable AI (Heatmap) <i class="fa-solid fa-circle-info"></i></div>
                <div class="upload-zone" style="margin-top: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 10px; cursor: pointer; padding: 25px; border-color: rgba(168,85,247,0.4);" onclick="openModal('mod-heatmap')">
                    <div style="position: relative; font-size: 3.5rem; color: #a855f7;">
                        <i class="fa-regular fa-map"></i>
                        <i class="fa-solid fa-magnifying-glass-plus" style="position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); font-size: 1.5rem; color: #fff;"></i>
                    </div>
                    <div style="font-size: 1.1rem; color: #e2e8f0; font-weight: 600;">Open AI Heatmap <i class="fa-solid fa-up-right-from-square" style="color: #60a5fa; font-size: 0.9rem; margin-left: 5px;"></i></div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Click to reveal XAI Analysis</div>
                </div>
            </div>
        </div>

        <!-- COLUMN 2: MIDDLE (Live Accuracy & Graphs) -->
        <div style="display: flex; flex-direction: column; gap: 1.2rem;">
            <!-- Live Accuracy -->
            <div class="widget" style="background: rgba(16, 13, 26, 0.85); box-shadow: 0 0 30px rgba(234, 179, 8, 0.2);">
                <div class="widget-title">
                    <span><i class="fa-solid fa-gauge" style="color:#eab308;"></i> Live Accuracy <i class="fa-solid fa-circle-info"></i></span>
                    <button class="btn btn-secondary" onclick="refreshAccuracy(this)"><i class="fa-solid fa-rotate-right" id="refresh-icon"></i> Refresh</button>
                </div>
                <div style="position:relative; height: 180px; width: 100%; display:flex; justify-content:center; margin-top:20px;">
                    <canvas id="liveGaugeCenter"></canvas>
                    <div style="position:absolute; bottom:15px; text-align:center; cursor:pointer;" onclick="openModal('mod-metrics')">
                        <span style="font-size:3.5rem; font-weight:900; color:#eab308; text-shadow: 0 0 25px rgba(234, 179, 8, 0.4);" id="cen-live">74.93%</span><br>
                        <span style="font-size:0.85rem; color:#94a3b8; font-weight:600; background:rgba(0,0,0,0.5); padding:4px 12px; border-radius:20px;">302 / 403 <i class="fa-solid fa-expand" style="color:#3b82f6;"></i></span>
                    </div>
                </div>
            </div>

            <!-- Accuracy Trend Graph -->
            <div class="widget" style="padding:15px; background:rgba(16, 13, 26, 0.7);">
                <div class="widget-title">
                    <span>Accuracy Trend Graph <i class="fa-solid fa-chart-line" style="color:#3b82f6;"></i></span>
                    <button class="btn btn-secondary" style="font-size:0.7rem; padding:4px 8px;" onclick="downloadChart('accCurveChart', 'Accuracy_History.png')"><i class="fa-solid fa-download"></i> Image</button>
                </div>
                <div style="height:220px; position:relative; width:100%;"><canvas id="accCurveChart"></canvas></div>
            </div>
            
            <!-- Loss Curve Graph -->
            <div class="widget" style="padding:15px; background:rgba(16, 13, 26, 0.7);">
                <div class="widget-title">
                    <span>Loss Curve Graph <i class="fa-solid fa-chart-area" style="color:#ef4444;"></i></span>
                    <button class="btn btn-secondary" style="font-size:0.7rem; padding:4px 8px;" onclick="downloadChart('lossCurveChart', 'Loss_History.png')"><i class="fa-solid fa-download"></i> Image</button>
                </div>
                <div style="height:220px; position:relative; width:100%;"><canvas id="lossCurveChart"></canvas></div>
            </div>
             
             <!-- Real-Time Logs Detail -->
            <div class="widget" style="flex:1;">
                <div class="widget-title">Real-Time Logs <i class="fa-solid fa-list"></i></div>
                <div class="upload-zone" style="margin-top: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 10px; cursor: pointer; padding: 25px; border-color: rgba(239,68,68,0.4);" onclick="openModal('mod-realtime-logs')">
                    <div style="position: relative; font-size: 3.5rem; color: #ef4444;">
                        <i class="fa-solid fa-clipboard-list"></i>
                        <i class="fa-solid fa-bug" style="position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); font-size: 1.5rem; color: #fff;"></i>
                    </div>
                    <div style="font-size: 1.1rem; color: #e2e8f0; font-weight: 600;">Open Server Logs <i class="fa-solid fa-up-right-from-square" style="color: #60a5fa; font-size: 0.9rem; margin-left: 5px;"></i></div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Click to reveal Server Events</div>
                </div>
            </div>
        </div>

        <!-- COLUMN 3: RIGHT -->
        <div style="display: flex; flex-direction: column; gap: 1.2rem;">
            <!-- Real-Time Progress -->
            <div class="widget">
                <div class="widget-title">
                    <span><i class="fa-solid fa-list-ol" style="color:#34d399;"></i> Real-Time Logs <i class="fa-solid fa-circle-info"></i></span>
                    <button class="btn btn-secondary" style="font-size:0.7rem;" onclick="simulateProgress()"><i class="fa-solid fa-arrow-up"></i> Progress</button>
                </div>
                <div style="display:flex; flex-direction:column; gap:15px; margin: 10px 0;">
                    <div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-weight:600; font-size:0.8rem; color:#cbd5e1;"><span>Epoch</span> <span style="color:#f59e0b; text-shadow:0 0 5px #f59e0b;">51.7%</span></div>
                        <div class="progress-bar-bg"><div class="progress-fill prog-orange" style="width:51.7%;"></div></div>
                    </div>
                    <div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-weight:600; font-size:0.8rem; color:#cbd5e1;"><span>Batch</span> <span style="color:#8b5cf6; text-shadow:0 0 5px #8b5cf6;">12.0%</span></div>
                        <div class="progress-bar-bg"><div class="progress-fill prog-purple" style="width:12%;"></div></div>
                    </div>
                </div>
                <div style="font-size:0.75rem; color:#94a3b8; padding-top:10px; border-top:1px dashed rgba(255,255,255,0.1);"><i class="fa-solid fa-server" style="color:#64748b;"></i> Epoch executed smoothly, internally processed accurately.</div>
            </div>

            <!-- Model Version Tracking -->
            <div class="widget">
                <div class="widget-title">
                    <span><i class="fa-solid fa-code-branch" style="color:#a855f7;"></i> Model Version v2.1.0</span>
                    <span class="btn btn-secondary" style="padding:4px 8px;" onclick="alert('Checking main branch for active model updates...')"><i class="fa-solid fa-list-check" style="color:#4ade80;"></i> Update</span>
                </div>
                <div style="display:flex; gap:8px; margin: 5px 0 15px 0;">
                    <div class="badge" style="background:#8b5cf6; color:#fff; box-shadow:0 0 10px #8b5cf6;"><i class="fa-solid fa-plus"></i> Quantum N.N.</div>
                    <div class="badge" style="background:rgba(255,255,255,0.1); color:#e2e8f0;">4 GNM</div>
                    <div class="badge" style="background:rgba(16,185,129,0.2); color:#4ade80; border:1px solid #10b981;">2.23</div>
                    <div class="badge" style="background:rgba(255,255,255,0.1); color:#e2e8f0;">V6.0</div>
                </div>
                <div class="terminal-logs" id="realtime-logs-box" style="background:rgba(0,0,0,0.6); padding:15px; border-radius:8px; border:1px solid #000; height:120px; overflow-y:auto; box-shadow:inset 0 0 20px rgba(0,0,0,1);">
                    <div class="ok"><i class="fa-solid fa-check"></i> System initialized. Monitoring Live Inferences...</div>
                </div>
            </div>
            
            <!-- Dataset Distribution Graph -->
            <div class="widget">
                <div class="widget-title">
                    <span><i class="fa-solid fa-chart-column" style="color:#3b82f6;"></i> Dataset Distrobution <i class="fa-solid fa-circle-question"></i></span>
                    <div style="display:flex; gap:5px;"><span class="badge" style="background:rgba(255,255,255,0.1); cursor:pointer;" onclick="alert('Distribution logs currently being mapped.')">GLog</span> <span class="badge btn-primary" style="cursor:pointer;" onclick="alert('Changing dataset view mode.')"><i class="fa-solid fa-eye"></i></span></div>
                </div>
                <div style="height:150px; position:relative; background:rgba(0,0,0,0.3); padding:10px; border-radius:8px; border:1px solid rgba(255,255,255,0.05);">
                    <canvas id="barChartDummy"></canvas>
                </div>
            </div>

            <!-- Prediction History Tracking -->
            <div class="widget" style="flex:1;">
                <div class="widget-title">Prediction History <i class="fa-solid fa-clock-rotate-left"></i></div>
                <div class="upload-zone" style="margin-top: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 10px; cursor: pointer; padding: 25px; border-color: rgba(139,92,246,0.4);" onclick="openModal('mod-history')">
                    <div style="position: relative; font-size: 3.5rem; color: #8b5cf6;">
                        <i class="fa-regular fa-clipboard"></i>
                        <i class="fa-solid fa-clock-rotate-left" style="position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); font-size: 1.5rem; color: #fff;"></i>
                    </div>
                    <div style="font-size: 1.1rem; color: #e2e8f0; font-weight: 600;">Open Prediction History <i class="fa-solid fa-up-right-from-square" style="color: #60a5fa; font-size: 0.9rem; margin-left: 5px;"></i></div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Click to reveal Global Ledger</div>
                </div>
            </div>

            <canvas id="liveGaugeRight" style="display:none;"></canvas>
            <span id="r-live" style="display:none;"></span>
        </div>
    </div>
"""

with open(r'c:\Users\91817\OneDrive\Documents\Desktop\BinaryImageQNN\assets\templates\users\qnn_results.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('    <div class="dashboard-grid">')
end_idx = text.find('    <!-- Footer Sound Control -->')

new_text = text[:start_idx] + content + "\n\n" + text[end_idx:]

with open(r'c:\Users\91817\OneDrive\Documents\Desktop\BinaryImageQNN\assets\templates\users\qnn_results.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Done")
