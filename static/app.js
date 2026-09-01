/**
 * CineOps AI - Web Dashboard Logic & API Integration
 */

const SAMPLE_SCREENPLAY = `SCENARIO TITLE: SHADOWS OVER METROPOLIS

INT. POLICE PRECINCT - OFFICE - NIGHT

Rain lashes against the windowpanes of the precinct office. DETECTIVE MILLER (40s, weary, wearing a wet leather trench coat) stares at a TABLET COMPUTER showing encrypted evidence.

CAPTAIN HENDERSON enters, tossing a fresh CASE FILE FOLDER onto the wooden desk beside Miller's steaming COFFEE CUP.

                    HENDERSON
          The Mayor's office wants this closed 
          before sunrise, Miller. No excuses.

Miller grabs his VISHNU VINTAGE REVOLVER from the desk drawer and holsters it.

                    MILLER
          Then we better head to the alleyway now.


EXT. ABANDONED ALLEYWAY - NIGHT

Heavy rain pours down continuously. Water splashes under boot heels. Low ground fog covers the cobblestones. 

Miller and OFFICER DAVIS stand over a shattered crate. Miller clicks on a high-intensity FLASHLIGHT, illuminating tyre tracks leading toward the warehouse.

                    DAVIS
          Ground is slick, Detective. Careful near 
          that unstable fire escape overhead.

Miller picks up a metallic fragment with tweezers and drops it into a plastic EVIDENCE BAG.


EXT. WAREHOUSE ROOFTOP - DAWN

The first dim rays of dawn break over the skyline. High wind sweeps across the roof perimeter.

SUSPECT X stands near the roof edge holding a SNIPER RIFLE and a SMOKE GRENADE. 

Miller steps out onto the roof, gun drawn.

                    MILLER
          Step away from the edge!

Suspect X pulls the pin on the smoke grenade—thick red smoke explodes across the roof. Stunt doubles prepare for a high fall as pyrotechnic squibs detonate along the brick chimney.`;

let currentAnalysisData = null;
let currentPlanData = null;

let selectedPdfFile = null;

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", () => {
  checkBackendHealth();
  setupEventListeners();
  setupPdfUploadListeners();
});

// Check API Health Status
async function checkBackendHealth() {
  const statusBadge = document.getElementById("backend-status");
  try {
    const res = await fetch("/health");
    if (res.ok) {
      const data = await res.json();
      statusBadge.innerHTML = `
        <span class="status-dot online"></span>
        <span class="status-text">${data.service} - Online (Mock Mode)</span>
      `;
    } else {
      throw new Error("HTTP Status " + res.status);
    }
  } catch (err) {
    statusBadge.innerHTML = `
      <span class="status-dot offline"></span>
      <span class="status-text">Backend Offline</span>
    `;
  }
}

// Setup Event Listeners
function setupEventListeners() {
  // Load Sample Script
  document.getElementById("btn-load-sample").addEventListener("click", () => {
    document.getElementById("script-input").value = SAMPLE_SCREENPLAY.trim();
  });

  // Analyze Button (Text Input)
  document.getElementById("btn-analyze").addEventListener("click", handleAnalyzePipeline);

  // Analyze PDF Button
  document.getElementById("btn-analyze-pdf").addEventListener("click", handleAnalyzePdfPipeline);

  // Main Navigation Tabs
  document.getElementById("tab-input").addEventListener("click", () => switchView("input"));
  document.getElementById("tab-breakdown").addEventListener("click", () => switchView("breakdown"));
  document.getElementById("tab-plan").addEventListener("click", () => switchView("plan"));

  // Dashboard Sub-tabs
  document.querySelectorAll(".d-tab").forEach(tab => {
    tab.addEventListener("click", (e) => {
      document.querySelectorAll(".d-tab").forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".dtab-content").forEach(c => c.classList.remove("active"));
      
      e.target.classList.add("active");
      const targetId = "dtab-" + e.target.getAttribute("data-dtab");
      document.getElementById(targetId).classList.add("active");
    });
  });

  // Scene Filter Buttons
  document.querySelectorAll(".filter-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
      e.target.classList.add("active");
      filterScenes(e.target.getAttribute("data-filter"));
    });
  });
}

// Setup PDF Drag and Drop Listeners
function setupPdfUploadListeners() {
  const dropzone = document.getElementById("pdf-dropzone");
  const fileInput = document.getElementById("pdf-file-input");
  const removeBtn = document.getElementById("btn-remove-pdf");

  dropzone.addEventListener("click", (e) => {
    if (e.target.closest("#btn-remove-pdf")) return;
    fileInput.click();
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files[0]) {
      handlePdfFileSelected(e.target.files[0]);
    }
  });

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handlePdfFileSelected(e.dataTransfer.files[0]);
    }
  });

  removeBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    clearSelectedPdfFile();
  });
}

function handlePdfFileSelected(file) {
  if (!file.name.toLowerCase().endsWith(".pdf")) {
    alert("Invalid File: Uploaded file must be a PDF document (.pdf).");
    clearSelectedPdfFile();
    return;
  }

  if (file.size > 10 * 1024 * 1024) {
    alert("File Too Large: PDF file size exceeds the 10MB limit.");
    clearSelectedPdfFile();
    return;
  }

  selectedPdfFile = file;
  const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
  document.getElementById("pdf-filename").textContent = `${file.name} (${sizeMB} MB)`;
  document.getElementById("pdf-file-info").classList.remove("hidden");
  document.getElementById("btn-analyze-pdf").disabled = false;
}

function clearSelectedPdfFile() {
  selectedPdfFile = null;
  document.getElementById("pdf-file-input").value = "";
  document.getElementById("pdf-file-info").classList.add("hidden");
  document.getElementById("pdf-filename").textContent = "";
  document.getElementById("btn-analyze-pdf").disabled = true;
}

// View Switching
function switchView(viewName) {
  document.querySelectorAll(".view-section").forEach(sec => sec.classList.remove("active"));
  document.querySelectorAll(".nav-btn").forEach(btn => btn.classList.remove("active"));

  document.getElementById("section-" + viewName).classList.add("active");
  document.getElementById("tab-" + viewName).classList.add("active");
}

// Handle Full Pipeline Analysis Call
async function handleAnalyzePipeline() {
  const scriptText = document.getElementById("script-input").value.trim();

  if (!scriptText || scriptText.length < 10) {
    alert("Please enter or load screenplay text before running analysis.");
    return;
  }

  showProgressModal();

  try {
    // Stage 1 animation
    setStageState(1, "active");

    await delay(600);
    setStageState(1, "completed");
    setStageState(2, "active");

    // Stage 2 animation
    await delay(600);
    setStageState(2, "completed");
    setStageState(3, "active");

    // Call API
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        script_text: scriptText,
        mock_mode: true
      })
    });

    if (!response.ok) {
      throw new Error(`Pipeline API call failed: ${response.statusText}`);
    }

    currentPlanData = await response.json();
    
    // We also generate breakdown representation from plan details
    setStageState(3, "completed");
    await delay(400);
    hideProgressModal();

    // Enable tabs & render views
    document.getElementById("tab-breakdown").disabled = false;
    document.getElementById("tab-plan").disabled = false;

    renderProductionPlan(currentPlanData);

    // Also fetch standalone analysis for breakdown tab
    const analysisResponse = await fetch("/api/analyze-screenplay", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ script_text: scriptText, mock_mode: true })
    });
    
    if (analysisResponse.ok) {
      currentAnalysisData = await analysisResponse.json();
      renderScreenplayBreakdown(currentAnalysisData);
    }

    // Switch to Screenplay Breakdown view
    switchView("breakdown");

  } catch (err) {
    hideProgressModal();
    alert("Analysis Failed: " + err.message);
  }
}

// Handle PDF Screenplay Ingestion Pipeline Call
async function handleAnalyzePdfPipeline() {
  if (!selectedPdfFile) {
    alert("Please select a PDF file before starting analysis.");
    return;
  }

  showProgressModal();

  try {
    // Stage 1 animation
    setStageState(1, "active");
    await delay(600);
    setStageState(1, "completed");
    setStageState(2, "active");

    // Stage 2 animation
    await delay(600);
    setStageState(2, "completed");
    setStageState(3, "active");

    // Construct FormData
    const formData = new FormData();
    formData.append("file", selectedPdfFile);
    formData.append("mock_mode", "true");

    const response = await fetch("/api/analyze-pdf", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      let errDetail = response.statusText;
      try {
        const errJson = await response.json();
        if (errJson.detail) errDetail = errJson.detail;
      } catch (e) {}
      throw new Error(errDetail);
    }

    currentPlanData = await response.json();

    setStageState(3, "completed");
    await delay(400);
    hideProgressModal();

    // Enable tabs & render views
    document.getElementById("tab-breakdown").disabled = false;
    document.getElementById("tab-plan").disabled = false;

    renderProductionPlan(currentPlanData);

    // Also fetch sample breakdown representation for breakdown tab
    const analysisResponse = await fetch("/api/analyze-screenplay", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ script_text: SAMPLE_SCREENPLAY, mock_mode: true })
    });

    if (analysisResponse.ok) {
      currentAnalysisData = await analysisResponse.json();
      renderScreenplayBreakdown(currentAnalysisData);
    }

    // Switch to Screenplay Breakdown view
    switchView("breakdown");

  } catch (err) {
    hideProgressModal();
    alert("PDF Analysis Failed: " + err.message);
  }
}

// Render Screenplay Breakdown View
function renderScreenplayBreakdown(analysis) {
  // Render KPI Metrics
  document.getElementById("kpi-scenes").textContent = analysis.total_scenes;
  document.getElementById("kpi-cast").textContent = analysis.all_characters.length;
  document.getElementById("kpi-props").textContent = analysis.all_props.length;
  document.getElementById("kpi-risks").textContent = analysis.high_risk_scenes.length;

  // Render Scene Cards Grid
  const grid = document.getElementById("scenes-grid");
  grid.innerHTML = "";

  analysis.scenes.forEach(scene => {
    const card = document.createElement("div");
    card.className = "scene-card";
    card.setAttribute("data-loc", scene.location_type);
    card.setAttribute("data-tod", scene.time_of_day);

    const charsPills = scene.characters.map(c => `<span class="pill">${c}</span>`).join("");
    const propsPills = scene.props.map(p => `<span class="pill">${p}</span>`).join("");
    const weatherPills = scene.weather_environment.map(w => `<span class="pill">${w}</span>`).join("");
    const specPills = scene.special_production_requirements.map(s => `<span class="pill">${s}</span>`).join("");

    card.innerHTML = `
      <div class="scene-header">
        <span class="scene-number">SCENE ${scene.scene_number}</span>
        <div class="scene-badges">
          <span class="badge-tag">${scene.location_type}</span>
          <span class="badge-tag">${scene.time_of_day}</span>
        </div>
      </div>
      <div class="scene-title">${scene.location_name}</div>
      <p class="scene-desc">${scene.scene_description}</p>

      ${charsPills ? `<div><strong class="reasoning-label">Characters:</strong><div class="pill-group">${charsPills}</div></div>` : ""}
      ${propsPills ? `<div><strong class="reasoning-label">Props:</strong><div class="pill-group">${propsPills}</div></div>` : ""}
      ${weatherPills ? `<div><strong class="reasoning-label">Weather / Environment:</strong><div class="pill-group">${weatherPills}</div></div>` : ""}
      ${specPills ? `<div><strong class="reasoning-label">Special Specs:</strong><div class="pill-group">${specPills}</div></div>` : ""}
    `;
    grid.appendChild(card);
  });
}

// Render Production Plan Dashboard
function renderProductionPlan(plan) {
  document.getElementById("plan-title").textContent = plan.title;
  document.getElementById("plan-days-badge").textContent = `${plan.total_estimated_days} Shooting Days`;
  document.getElementById("plan-overall-summary").textContent = plan.overall_summary;
  document.getElementById("plan-strategic-reasoning").textContent = plan.strategic_reasoning;

  // 1. Shooting Schedule Timeline
  const scheduleTimeline = document.getElementById("schedule-timeline");
  scheduleTimeline.innerHTML = "";
  plan.shooting_schedule.forEach(day => {
    const card = document.createElement("div");
    card.className = "day-card";
    card.innerHTML = `
      <div class="day-info">
        <h4>${day.title}</h4>
        <p><strong>Scenes Scheduled:</strong> ${day.scene_numbers.join(", ")} | <strong>Location:</strong> ${day.location}</p>
        <p style="margin-top: 0.5rem;">${day.notes_and_rationale}</p>
      </div>
      <div class="day-meta">
        <span class="day-hours">${day.estimated_hours} Hours</span>
      </div>
    `;
    scheduleTimeline.appendChild(card);
  });

  // 2. Location Units
  const groupingsGrid = document.getElementById("groupings-grid");
  groupingsGrid.innerHTML = "";
  plan.scene_groupings.forEach(grp => {
    const card = document.createElement("div");
    card.className = "info-card";
    card.innerHTML = `
      <h4>${grp.group_name}</h4>
      <p><strong>Group ID:</strong> ${grp.group_id} | <strong>Location:</strong> ${grp.location_name}</p>
      <p><strong>Scenes Included:</strong> ${grp.scene_numbers.join(", ")}</p>
      <p style="margin-top:0.5rem;">${grp.grouping_reason}</p>
    `;
    groupingsGrid.appendChild(card);
  });

  // 3. Resource Matrix
  const resourcesGrid = document.getElementById("resources-grid");
  resourcesGrid.innerHTML = "";
  plan.resource_requirements.forEach(res => {
    const card = document.createElement("div");
    card.className = "info-card";
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h4>${res.item_name}</h4>
        <span class="badge badge-accent">${res.category}</span>
      </div>
      <p><strong>Required for Scenes:</strong> ${res.required_for_scenes.join(", ")}</p>
      <p style="margin-top:0.35rem;">${res.specification_details || ""}</p>
    `;
    resourcesGrid.appendChild(card);
  });

  // 4. Risk Management Matrix
  const risksGrid = document.getElementById("risks-grid");
  risksGrid.innerHTML = "";
  plan.production_risks.forEach(risk => {
    const card = document.createElement("div");
    card.className = `info-card sev-${risk.severity}`;
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h4>${risk.description}</h4>
        <span class="badge badge-warning">${risk.severity} SEVERITY</span>
      </div>
      <p><strong>Category:</strong> ${risk.risk_category}</p>
      <p style="margin-top:0.5rem;"><strong>Mitigation Plan:</strong> ${risk.mitigation_notes || 'Standard safety protocol'}</p>
    `;
    risksGrid.appendChild(card);
  });

  // 5. Parallel Research Hub
  const researchGrid = document.getElementById("research-grid");
  researchGrid.innerHTML = "";
  plan.research_references.forEach(ref => {
    const card = document.createElement("div");
    card.className = "info-card";
    card.innerHTML = `
      <h4>${ref.title}</h4>
      <p><strong>Topic:</strong> ${ref.topic}</p>
      <p style="margin: 0.5rem 0;"><em>"${ref.key_insight}"</em></p>
      <a href="${ref.url}" target="_blank" rel="noopener" class="btn btn-secondary btn-sm" style="margin-top:0.5rem;">View Parallel Citation</a>
    `;
    researchGrid.appendChild(card);
  });
}

// Scene Filtering Logic
function filterScenes(filter) {
  const cards = document.querySelectorAll(".scene-card");
  cards.forEach(card => {
    const loc = card.getAttribute("data-loc");
    const tod = card.getAttribute("data-tod");

    if (filter === "all") {
      card.style.display = "flex";
    } else if (filter === "INT" || filter === "EXT") {
      card.style.display = (loc === filter) ? "flex" : "none";
    } else if (filter === "NIGHT") {
      card.style.display = (tod === "NIGHT") ? "flex" : "none";
    }
  });
}

// Modal Helpers
function showProgressModal() {
  document.getElementById("progress-modal").classList.add("active");
  resetStageStates();
}

function hideProgressModal() {
  document.getElementById("progress-modal").classList.remove("active");
}

function resetStageStates() {
  for (let i = 1; i <= 3; i++) {
    const el = document.getElementById(`stage-${i}`);
    el.className = "stage-item";
  }
}

function setStageState(stageNum, state) {
  const el = document.getElementById(`stage-${stageNum}`);
  if (el) {
    el.className = `stage-item ${state}`;
  }
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
