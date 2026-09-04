# CineOps AI

> An agentic AI production command center that turns screenplay PDFs into actionable, research-backed shooting plans.

---

## 1. Problem

Film production teams face immense complexity when translating creative screenplays into execution-ready shooting plans. Assistant Directors (ADs), Line Producers, and Unit Production Managers (UPMs) must manually read screenplays scene-by-scene to identify:

- **Locations & Set Types** (INT/EXT, Day/Night)
- **Cast & Characters** required per scene
- **Props, Vehicles, and Costumes**
- **Weather, Environment, and Time-of-Day constraints**
- **Special Production Specs** (stunts, rain machines, high falls, pyrotechnics)
- **Safety Risks & Environmental Hazards**
- **Equipment & Crew Resource Needs**
- **Location Unit Groupings & Shooting Schedules**
- **External Legal & Technical Research Requirements** (permits, safety codes)

As screenplays grow to dozens or hundreds of pages, manual breakdowns become prone to human oversight, scheduling conflicts, safety oversights, and budget overruns.

---

## 2. Solution

**CineOps AI** automates screenplay production management through an end-to-end agentic workflow.

Filmmakers can upload raw screenplay text or PDF files and receive a structured production breakdown, real-world production research, risk analysis, resource requirements, and an actionable shooting plan.

### High-Level Workflow

```text
Screenplay PDF / Text Ingestion
  └──▶ PDFExtractorService
        └──▶ Screenplay Analyst Agent (Google ADK)
              └──▶ 11-Parameter Scene Production Breakdown
                    └──▶ Dynamic Parallel Search Research
                          └──▶ Production Research & Guidelines
                                └──▶ Production Planner Agent (Google ADK)
                                      └──▶ Production Plan Dashboard
```

CineOps AI transforms unstructured screenplay prose into structured production intelligence, helping filmmakers move from screenplay to production-ready decisions.

---

## 3. Key Features

- **PDF Screenplay Upload**: Native drag-and-drop PDF ingestion powered by `pypdf` via `PDFExtractorService`, supporting files up to 10MB.
- **Direct Text Analysis**: Plaintext screenplay input for fast local testing and development.
- **11-Parameter Scene Breakdown**: Autonomous extraction of scene numbers, location type, location name, time of day, scene summary, characters, props, weather/environment, special production requirements, production dependencies, and production risks.
- **Dynamic Parallel Web Research**: Uses the official Parallel Search API to research screenplay-specific production requirements instead of relying on generic research queries.
- **Smart Scene Grouping**: Groups scenes by compatible locations and production requirements to reduce unnecessary unit moves.
- **Day-by-Day Shooting Schedule**: Generates structured shooting-day allocations based on scene and production constraints.
- **Resource Matrix**: Identifies production-relevant equipment, crew, props, lighting, stunt, and special-effect requirements.
- **Risk Management Matrix**: Categorizes production risks as CRITICAL, HIGH, MEDIUM, or LOW with actionable mitigation guidance.
- **Parallel Research References**: Provides research results and citations that support production decisions.
- **Cinematic Production Dashboard**: Dark, production-focused web interface with responsive cards, filters, progress states, schedules, resources, and risk management.
- **FastAPI REST API**: Structured REST endpoints with Pydantic validation.
- **Optional Offline Development Mode**: Deterministic mock mode is available for local development and testing without external API calls. Production runs with live Gemini and Parallel integrations.

---

## 4. Agentic Workflow

CineOps AI is built using a multi-agent modular architecture powered by the Google Agent Development Kit (ADK), Gemini 2.5 Flash, and the Parallel Search API.

```text
┌─────────────────────────────────────────────────────────┐
│                 Screenplay Ingestion                     │
│          (Text Input or PDF File Upload)                 │
└────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│               PDFExtractorService                        │
│        (Extracts screenplay text from PDF)               │
└────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│            Screenplay Analyst Agent                      │
│    (Google ADK / Gemini 2.5 Flash via Vertex AI)         │
│    - Extracts structured scene information                │
│    - Identifies production requirements & hazards         │
└────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│            ScreenplayProductionAnalysis                  │
│         (Validated Pydantic Data Model)                  │
└────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│             Parallel Search Service                      │
│        (Official Parallel Search API)                    │
│    - Generates screenplay-specific research queries        │
│    - Deduplicates relevant research requests               │
│    - Returns structured research results                   │
└────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│            Production Research Data                      │
│         (ProductionResearchResponse Model)                │
└────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│            Production Planner Agent                      │
│    (Google ADK / Gemini 2.5 Flash via Vertex AI)          │
│    - Synthesizes analysis + research                      │
│    - Groups scenes and locations                          │
│    - Generates schedule, resources & risks                 │
└────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│                 ProductionPlan                            │
│          (Validated Pydantic Model)                       │
└────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│             CineOps AI Web Dashboard                      │
│       (Interactive Production Command Center)              │
└─────────────────────────────────────────────────────────┘
```

### Component Responsibilities

- **PDFExtractorService**: Extracts screenplay text from uploaded PDF byte streams.
- **Screenplay Analyst Agent**: Uses Google ADK and Gemini 2.5 Flash to convert screenplay text into structured `ScreenplayProductionAnalysis`.
- **Parallel Search Service**: Performs screenplay-specific web research for production safety, technical requirements, regulations, permits, and other relevant constraints.
- **Production Planner Agent**: Combines screenplay analysis and external research to construct an actionable `ProductionPlan`.
- **Production Planner Service**: Reconciles locations, scenes, resources, risks, and schedule information so important screenplay details are not silently dropped.

---

## 5. Google Cloud / Gemini Integration

CineOps AI uses Google Cloud and Gemini AI technologies as core components of its production workflow.

- **Google Cloud Vertex AI**: Provides the runtime environment for Gemini model execution.
- **Google Agent Development Kit (ADK)**: Provides the agent framework, tools, prompts, and orchestration layer.
- **Gemini 2.5 Flash**: Used by the Screenplay Analyst Agent and Production Planner Agent.
- **Google Cloud Authentication**: Uses Application Default Credentials (ADC) for Cloud Run deployment.
- **Production Project**: `cineops-ai-507217`
- **Production Region**: `us-central1`
- **Production Execution Mode**: `CINEOPS_MOCK_MODE=0`

### Live Production Status

CineOps AI is deployed on Google Cloud Run and runs with live Gemini 2.5 Flash through Vertex AI.

The production pipeline is:

```text
Screenplay
    ↓
Gemini Screenplay Analysis
    ↓
Parallel Search Research
    ↓
Gemini Production Planning
    ↓
Production Plan
```

Local development can optionally use deterministic mock mode to avoid external API calls.

---

## 6. Parallel Integration

CineOps AI integrates the official Parallel Search API using the `parallel-web` SDK to provide real-world production research.

### Dynamic Research

Research queries are derived from the actual screenplay analysis rather than using a single hardcoded research topic.

Depending on screenplay content, CineOps can research areas such as:

- Rain / Wet-Location Safety
- Electrical Safety
- Drone Filming Requirements
- Working-at-Height Safety
- Stunt and Fall Protection
- Pyrotechnic / Special Effects Requirements
- Water-Side Filming Considerations
- Weather-Related Production Constraints
- Technical Equipment Requirements
- Permits and Regulatory Requirements

The system deduplicates repeated research requirements within a production-planning request to reduce unnecessary external calls.

### Live API Verification

The Parallel Search integration has been verified against the official Parallel Search API with successful structured search responses.

The application uses the Parallel API at runtime rather than simply mentioning Parallel in documentation.

The Parallel API key is stored as an environment variable / managed secret and is never hardcoded into source code or returned through API responses.

---

## 7. Tech Stack

| Layer | Technology |
|---|---|
| AI Agents & Framework | Google Agent Development Kit (ADK) |
| LLM Model | Gemini 2.5 Flash via Google Cloud Vertex AI |
| Cloud Infrastructure | Google Cloud Platform / Cloud Run / Vertex AI |
| External Web Research | Parallel Search API (parallel-web) |
| Backend Framework | FastAPI |
| Language & Runtime | Python 3.10+ |
| Data Validation | Pydantic v2 |
| PDF Extraction | pypdf |
| Frontend UI | HTML5, CSS3, JavaScript (ES6) |
| ASGI Web Server | Uvicorn |
| Containerization | Docker |
| Testing | Pytest |

---

## 8. Project Structure

```text
cineops/
├── .env                    # Local environment variables (Git-ignored)
├── .env.example            # Environment configuration template
├── .gitignore              # Git ignore configuration
├── LICENSE                 # MIT License
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── cineops_agent.py
│   │   ├── production_planner_agent.py
│   │   └── screenplay_agent.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── schemas.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── planner.py
│   │   ├── production.py
│   │   └── screenplay.py
│   └── services/
│       ├── __init__.py
│       ├── parallel_search.py
│       ├── pdf_extractor.py
│       ├── production_planner_service.py
│       └── screenplay_parser.py
├── static/
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── tests/
    ├── __init__.py
    ├── fixtures/
    ├── test_api.py
    ├── test_parallel_search.py
    ├── test_pdf_api.py
    ├── test_production_planner.py
    └── test_screenplay_analysis.py
```

---

## 9. API Documentation

### 1. Health Status Check

- **Endpoint**: `GET /health`
- **Purpose**: Verifies backend service availability.
- **Output**:

```json
{
  "status": "ok",
  "service": "cineops-ai"
}
```

### 2. Screenplay Text Analysis

- **Endpoint**: `POST /api/analyze-screenplay`
- **Purpose**: Extracts a structured screenplay production breakdown from screenplay text.
- **Response**: `ScreenplayProductionAnalysis` object containing detailed scene information.

### 3. Generate Production Plan

- **Endpoint**: `POST /api/generate-plan`
- **Purpose**: Generates a production plan from screenplay analysis and optional research data.
- **Response**: `ProductionPlan` object.

### 4. Combined Text Pipeline

- **Endpoint**: `POST /api/analyze`
- **Purpose**: Executes the complete workflow: Screenplay Analyst → Parallel Research → Production Planner
- **Response**: `ProductionPlan` containing both the production plan and screenplay analysis.

### 5. PDF Screenplay Upload Pipeline

- **Endpoint**: `POST /api/analyze-pdf`
- **Purpose**: Accepts a screenplay PDF, extracts its text, analyzes the actual uploaded screenplay, performs relevant production research, and generates the production plan.
- **Input**: `multipart/form-data` with `file` (PDF up to 10MB).
- **Response**: `ProductionPlan` containing screenplay analysis, schedule, locations, resources, risks, and research references.

---

## 10. Local Setup

### Prerequisites

- Python 3.10 or higher
- Git

### Installation Steps

**Clone Repository**

```bash
git clone https://github.com/aastha-yadav2/CineopsAI.git
cd CineopsAI
```

**Create Virtual Environment**

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Install Dependencies**

```bash
pip install -r requirements.txt
```

**Configure Environment Variables**

Create a `.env` file based on `.env.example`:

```env
# Google Cloud / Vertex AI
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=cineops-ai-507217
GOOGLE_CLOUD_LOCATION=us-central1
CINEOPS_GEMINI_MODEL=gemini-2.5-flash

# Execution Mode
# 1 = Offline mock mode for local development
# 0 = Live Gemini + Parallel Search
CINEOPS_MOCK_MODE=1

# Parallel Search API
PARALLEL_API_KEY=your_parallel_api_key_here
```

For local development, `CINEOPS_MOCK_MODE=1` can be used for deterministic offline testing.

The deployed production environment runs with `CINEOPS_MOCK_MODE=0`.

---

## 11. Running the Application

Launch the FastAPI application locally using Uvicorn:

```bash
.venv\Scripts\python.exe -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

### Local Access Points

- **Web Command Center**: http://127.0.0.1:8000/
- **Interactive API Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

### Live Demo

The deployed CineOps AI application is available at:

https://cineops-ai-408484150701.us-central1.run.app

### User Journeys

**Text Screenplay Flow**

1. Open the CineOps AI dashboard.
2. Enter screenplay text or use "Try Example Script".
3. Click "Analyze Screenplay & Build Plan".
4. Review the screenplay breakdown.
5. Explore the generated production plan.

**PDF Screenplay Flow**

1. Open the CineOps AI dashboard.
2. Drag and drop a `.pdf` screenplay into the upload area.
3. Click "Analyze PDF Screenplay".
4. Wait for the analysis stages to complete.
5. Review the screenplay breakdown.
6. Explore locations, resources, risks, schedule, and Parallel research.

---

## 12. Testing

CineOps AI includes an automated test suite with deterministic offline mock execution for local testing.

Run:

```bash
.venv\Scripts\python.exe -m pytest tests/ -v
```

The test suite covers screenplay analysis, PDF extraction, API behavior, production planning, and Parallel Search integration behavior.

Production verification additionally includes live Cloud Run endpoint testing with `CINEOPS_MOCK_MODE=0`.

---

## 13. Security

- **Git Exclusion**: `.env`, `.venv`, and other local development artifacts are excluded through `.gitignore`.
- **Environment Variables**: Credentials and configuration are loaded through environment variables.
- **Managed Production Secret**: The Parallel Search API key is provided to the Cloud Run service through managed secret configuration.
- **Zero Credential Exposure**: API keys are never returned in REST responses or intentionally logged.
- **Offline Development Mode**: Local mock mode can be used to avoid unintended external API calls during development.
- **Production Mode**: The deployed application uses live Gemini and Parallel integrations.

---

## 14. Hackathon Requirement Mapping

| Requirement | CineOps AI Implementation |
|---|---|
| Gemini / Google Cloud | Gemini 2.5 Flash through Vertex AI with Google ADK |
| Agentic Workflow | Screenplay Analyst Agent + Production Planner Agent |
| Partner Integration | Official Parallel Search API via parallel-web |
| Real Media Workflow | Converts screenplay PDFs into structured production plans |
| Web Dashboard | Interactive production command center served through FastAPI |
| Open Source Repository | Public GitHub repository with MIT License and automated tests |

---

## 15. Why This Is Agentic

CineOps AI goes beyond a single LLM prompt or basic text summarization.

### 1. Multi-Agent Decomposition

The system separates screenplay understanding from production planning.

- Screenplay Analyst Agent identifies production-critical information.
- Production Planner Agent converts that information and external research into an actionable plan.

### 2. Autonomous Research

The workflow derives production research requirements from screenplay-specific hazards and technical constraints and uses the Parallel Search API to obtain relevant external information.

### 3. Structured State Synthesis

Pydantic models enforce structured data exchange between screenplay analysis, research, and production planning.

### 4. Production Reasoning

The system combines location, time, resources, hazards, dependencies, and research findings to construct a practical production schedule and risk-management plan.

### 5. Reconciliation

The production-planning layer reconciles extracted screenplay information with generated planning data so that important scenes, locations, and resources are not silently lost.

---

## 16. Demo Walkthrough

1. Open the CineOps AI Dashboard using the live Cloud Run deployment.
2. Upload a screenplay PDF or click "Try Example Script".
3. Start the screenplay analysis.
4. Observe the workflow progress:
   - Screenplay Analysis
   - Parallel Research
   - Production Planning
5. Review the Screenplay Breakdown:
   - Scenes
   - Locations
   - Characters
   - Props
   - Weather / Environment
   - Production Requirements
   - Risks
6. Explore the Production Plan:
   - Shooting Schedule
   - Location Units
   - Resource Matrix
   - Risk Management Matrix
   - Parallel Research Hub
7. Review research-backed recommendations and production constraints.

### Core Demo Story

```text
SCREENPLAY PDF
      ↓
AI SCREENPLAY ANALYSIS
      ↓
SCREENPLAY-SPECIFIC PARALLEL RESEARCH
      ↓
AI PRODUCTION PLANNING
      ↓
RESEARCH-BACKED SHOOTING PLAN
```

---

## 17. Current Status & Roadmap

### Completed

- ✅ Screenplay text parsing and structured scene extraction
- ✅ 11-parameter screenplay production breakdown
- ✅ PDF screenplay ingestion
- ✅ Google ADK agent workflow
- ✅ Gemini 2.5 Flash through Vertex AI
- ✅ Official Parallel Search API integration
- ✅ Dynamic and deduplicated production research
- ✅ Production Planner agent
- ✅ Location and scene reconciliation
- ✅ Resource reconciliation
- ✅ Risk management
- ✅ Shooting schedule generation
- ✅ FastAPI backend
- ✅ Production command center dashboard
- ✅ Offline automated testing
- ✅ Docker containerization
- ✅ Google Cloud Run deployment
- ✅ Live production execution with `CINEOPS_MOCK_MODE=0`

### Roadmap

- Intelligent location scouting
- Crew and equipment optimization
- Budget estimation
- Permit and compliance workflows
- Automated call-sheet generation
- Weather-aware scheduling
- Advanced production cost forecasting
- Collaborative production planning for film teams

---

## 18. License

This project is open-source and licensed under the MIT License.

See the `LICENSE` file in the repository root for the full license text.

---

## 19. Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Add or update tests where appropriate.
5. Submit a pull request.

Please open an issue for bugs, feature requests, or technical discussions.

---

## 20. Acknowledgements

- **Google Cloud & Vertex AI** — for Gemini infrastructure and cloud deployment.
- **Google ADK** — for agent orchestration and tool-based workflows.
- **Gemini 2.5 Flash** — for screenplay analysis and production planning.
- **Parallel** — for real-time external web research.
- **FastAPI & Pydantic** — for backend API infrastructure and structured validation.
- **pypdf** — for screenplay PDF extraction.

---

## Live Demo

**CineOps AI**: https://cineops-ai-408484150701.us-central1.run.app

**GitHub Repository**: https://github.com/aastha-yadav2/CineopsAI

**License**: MIT
