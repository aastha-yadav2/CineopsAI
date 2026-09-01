# CineOps AI

> An agentic AI production command center that turns screenplay PDFs into actionable shooting plans.

---

## 1. Problem

Film production teams face immense complexity when translating creative screenplays into execution-ready shooting plans. Assistant Directors (ADs), Line Producers, and Unit Production Managers (UPMs) must manually read screenplays scene-by-scene to identify:

* **Locations & Set Types** (INT/EXT, Day/Night)
* **Cast & Characters** required per scene
* **Props, Vehicles, and Costumes**
* **Weather, Environment, and Time-of-Day constraints**
* **Special Production Specs** (stunts, rain machines, high falls, pyrotechnics)
* **Safety Risks & Environmental Hazards**
* **Equipment & Crew Resource Needs**
* **Location Unit Groupings & Shooting Schedules**
* **External Legal & Technical Research Requirements** (permits, safety codes)

As screenplays grow to dozens or hundreds of pages, manual breakdowns become prone to human oversight, costly scheduling conflicts, safety oversights, and budget overruns.

---

## 2. Solution

**CineOps AI** automates and elevates screenplay production management through an end-to-end agentic workflow. Filmmakers can upload raw screenplay text or PDF files and receive a structured, highly optimized production plan within seconds.

### High-Level Workflow

```text
Screenplay PDF / Text Ingestion
  └──▶ PDFExtractorService
        └──▶ Screenplay Analyst Agent (Google ADK)
              └──▶ 11-Parameter Scene Production Breakdown
                    └──▶ Parallel Search Service (Official Parallel Web API)
                          └──▶ Structured Web Research & Guidelines
                                └──▶ Production Planner Agent (Google ADK)
                                      └──▶ Actionable Production Plan Dashboard
```

CineOps AI transforms unstructured screenplay prose into structured production intelligence, allowing filmmakers to focus on creative vision while maintaining rigorous safety and operational standards.

---

## 3. Key Features

* **PDF Screenplay Upload**: Native drag-and-drop PDF ingestion powered by `pypdf` via `PDFExtractorService` (supporting files up to 10MB).
* **Direct Text Analysis**: Plaintext screenplay input for fast local testing and development.
* **11-Parameter Scene Breakdown**: Autonomous extraction of scene numbers, location type (INT/EXT), location name, time of day, scene summary, characters, props, weather/environment, special production requirements, hazards, and estimated shooting duration.
* **Parallel Web Research**: Autonomous execution of real-world external research via the official **Parallel Search API** for location safety rules, rain machine guidelines, GFCI electrical precautions, and drone filming permits.
* **Smart Scene Grouping**: Algorithmic consolidation of scenes sharing locations and lighting requirements to minimize unit moves.
* **Day-by-Day Shooting Schedule**: Intelligent daily breakdown balancing working hours and crew fatigue.
* **Resource Matrix**: Categorized breakdown of required camera gear, lighting packages, stunt equipment, and special effects.
* **Risk Management Matrix**: Categorized risk assessments (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) paired with actionable mitigation protocols.
* **Parallel Research References**: Linked research citations and key insights for production safety officers.
* **Cinematic Dark Web Dashboard**: Single-page production command center built with custom CSS glassmorphism, responsive grids, and live API stage progress animations.
* **FastAPI REST API**: High-performance RESTful API with Pydantic request/response validation.
* **Mock/Offline Development Mode**: 100% deterministic local testing mode making zero external network calls while Google Cloud billing activation is pending.

---

## 4. Agentic Workflow

CineOps AI is built using a multi-agent modular architecture powered by the Google Agent Development Kit (ADK) and the Parallel Search API.

```text
┌─────────────────────────────────────────────────────────┐
│                 Screenplay Ingestion                    │
│          (Text Input or PDF File Upload)                │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│               PDFExtractorService                       │
│        (Extracts raw plain text streams)                │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│            Screenplay Analyst Agent                     │
│    (Google ADK Agent / Gemini 2.5 Flash Model)          │
│    - Extracts 11-parameter scene breakdown              │
│    - Identifies production requirements & hazards       │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│            ScreenplayProductionAnalysis                 │
│         (Validated Pydantic Data Model)                 │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│             Parallel Search Service                     │
│    (Official Parallel Search Web API)                   │
│    - Performs targeted production safety searches       │
│    - Fetches ranked excerpts & search IDs               │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│            Production Research Data                     │
│         (ProductionResearchResponse Model)              │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│            Production Planner Agent                     │
│    (Google ADK Agent / Gemini 2.5 Flash Model)          │
│    - Synthesizes analysis + research                    │
│    - Groups scenes by location unit                     │
│    - Generates shooting schedule, resources & risks     │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                 ProductionPlan                          │
│          (Validated Pydantic Model)                     │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│             CineOps AI Web Dashboard                    │
│       (Interactive Command Center Interface)            │
└─────────────────────────────────────────────────────────┘
```

### Component Responsibilities

1. **`PDFExtractorService`**: Extracts clean screenplay text from PDF byte streams.
2. **`Screenplay Analyst Agent`**: Parses raw screenplay text into structured `ScreenplayProductionAnalysis` models.
3. **`Parallel Search Service`**: Queries the Parallel Search API to gather safety regulations, electrical codes, and filming permit details.
4. **`Production Planner Agent`**: Synthesizes the breakdown and research data to construct an optimized `ProductionPlan`.

---

## 5. Google Cloud / Gemini Integration

CineOps AI is designed from the ground up to utilize Google Cloud and Gemini AI technologies:

* **Google Cloud Vertex AI**: Hosted foundation for enterprise AI agent execution (`GOOGLE_GENAI_USE_VERTEXAI=TRUE`).
* **Google Agent Development Kit (ADK)**: Core agent framework defining system prompts, tools, and execution flows (`google-genai`).
* **Gemini Model Configuration**: Configurable via `CINEOPS_GEMINI_MODEL=gemini-2.5-flash` environment variable.
* **Google Cloud Authentication**: Integrates via Application Default Credentials (ADC) for seamless deployment to Google Cloud Run.
* **Configured Project & Region**: Project `cineops-ai-507217`, Location `us-central1`.

> [!NOTE]
> **Billing Status Notice**: Gemini live execution via Vertex AI is fully implemented and configured in the agent codebase (`src/agents/screenplay_agent.py` and `src/agents/production_planner_agent.py`). However, live Gemini API calls are currently disabled in local testing (`CINEOPS_MOCK_MODE=1`) while Google Cloud billing activation is pending.

---

## 6. Parallel Integration

CineOps AI integrates the official **Parallel Search API** (`parallel-web` v1.3.3) to provide film production teams with real-time, external web research.

### Real Production Use Cases Tested

During production planning, the Parallel Research Service queries web sources for:
* **Rain Machine Safety**: GFCI electrical protection rules and wet-down set precautions.
* **Night Shooting Hazards**: Lighting rig grounding and temporary power distribution codes.
* **Drone Filming Permits**: FAA Part 107 licensing and commercial airspace clearance.
* **Pyrotechnic & Stunt Protocols**: Fire marshal presence and emergency fall protection.

### Live API Verification

The Parallel Search integration has been verified live against `api.parallel.ai`:
* **HTTP Status**: `200 OK`
* **Search ID**: `search_68fe02dd7627645cefdf687e51402f0a`
* **Results Returned**: 10 real-time structured search items with ranked excerpts and citations.

> [!IMPORTANT]
> The Parallel API key is read strictly from the local `.env` environment variable (`PARALLEL_API_KEY`) and is never committed, hardcoded, or exposed in API responses.

---

## 7. Tech Stack

| Layer | Technology |
| :--- | :--- |
| **AI Agents & Framework** | Google Agent Development Kit (ADK) (`google-genai`) |
| **LLM Model** | Gemini 2.5 Flash via Google Cloud Vertex AI |
| **Cloud Infrastructure** | Google Cloud Platform (Vertex AI, Cloud Run ready) |
| **External Web Research** | Parallel Search API (`parallel-web` SDK) |
| **Backend Framework** | FastAPI |
| **Language & Runtime** | Python 3.10+ |
| **Data Validation** | Pydantic v2 |
| **PDF Extraction** | `pypdf` via `PDFExtractorService` |
| **Frontend UI** | Vanilla HTML5, CSS3 (Glassmorphism), JavaScript (ES6) |
| **ASGI Web Server** | Uvicorn |
| **Test Suite** | Pytest (27 automated tests) |

---

## 8. Project Structure

```text
cineops/
├── .env                    # Local environment variables (Git-ignored)
├── .env.example            # Environment configuration template
├── .gitignore              # Git ignore configuration
├── README.md               # Hackathon project documentation
├── requirements.txt        # Python package dependencies
├── src/
│   ├── __init__.py
│   ├── main.py             # CLI entrypoint for local execution
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── cineops_agent.py             # Root agent definition
│   │   ├── production_planner_agent.py  # Production planning agent
│   │   └── screenplay_agent.py          # Screenplay analysis agent
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI application & route handlers
│   │   └── schemas.py          # Request and response API schemas
│   ├── models/
│   │   ├── __init__.py
│   │   ├── planner.py          # Production plan Pydantic models
│   │   ├── production.py       # Production breakdown models
│   │   └── screenplay.py       # Scene breakdown models
│   └── services/
│       ├── __init__.py
│       ├── parallel_search.py            # Parallel Search API service
│       ├── pdf_extractor.py              # pypdf extraction service
│       ├── production_planner_service.py # Planning service layer
│       └── screenplay_parser.py          # Screenplay parsing service layer
├── static/
│   ├── index.html          # Web dashboard layout
│   ├── styles.css          # Dark cinematic styling & components
│   └── app.js              # Web dashboard API & UI logic
└── tests/
    ├── __init__.py
    ├── fixtures/
    │   └── sample_screenplay.txt
    ├── test_api.py                 # REST API unit tests
    ├── test_parallel_search.py     # Parallel search service tests
    ├── test_pdf_api.py             # PDF extraction & PDF API tests
    ├── test_production_planner.py  # Production planner agent tests
    └── test_screenplay_analysis.py # Screenplay analyst agent tests
```

---

## 9. API Documentation

### 1. Health Status Check
* **Endpoint**: `GET /health`
* **Purpose**: Verifies backend API service availability.
* **Output**: `{"status": "ok", "service": "cineops-ai"}`

### 2. Screenplay Text Analysis
* **Endpoint**: `POST /api/analyze-screenplay`
* **Purpose**: Extracts structured 11-parameter breakdown from screenplay text.
* **Request Body**:
  ```json
  {
    "script_text": "INT. POLICE PRECINCT - NIGHT\nDetective Miller reads tablet.",
    "mock_mode": true
  }
  ```
* **Response**: `ScreenplayProductionAnalysis` object containing detailed scene breakdown array.

### 3. Generate Production Plan
* **Endpoint**: `POST /api/generate-plan`
* **Purpose**: Generates a production plan from pre-analyzed screenplay data and optional research.
* **Request Body**:
  ```json
  {
    "analysis": { ... },
    "research_data": null,
    "mock_mode": true
  }
  ```
* **Response**: `ProductionPlan` object.

### 4. Combined Text Pipeline
* **Endpoint**: `POST /api/analyze`
* **Purpose**: Executes full end-to-end pipeline (*Screenplay Analyst ➔ Parallel Research ➔ Production Planner*).
* **Request Body**:
  ```json
  {
    "script_text": "INT. POLICE PRECINCT - NIGHT\nDetective Miller inspects tablet.",
    "mock_mode": true
  }
  ```
* **Response**: `ProductionPlan` object.

### 5. PDF Screenplay Upload Pipeline
* **Endpoint**: `POST /api/analyze-pdf`
* **Purpose**: Accepts multipart PDF upload, extracts text, and executes the complete production planning pipeline.
* **Input**: `multipart/form-data` with `file` (PDF file up to 10MB) and optional `mock_mode` (`true`/`false`).
* **Response**: `ProductionPlan` object.

---

## 10. Local Setup

### Prerequisites
* Python 3.10 or higher
* Git

### Installation Steps

1. **Clone Repository**:
   ```bash
   git clone https://github.com/aastha-yadav2/CineopsAI.git
   cd CineopsAI
   ```

2. **Create Virtual Environment**:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the project root based on `.env.example`:
   ```env
   # Google Cloud / Vertex AI Authentication
   GOOGLE_GENAI_USE_VERTEXAI=TRUE
   GOOGLE_CLOUD_PROJECT=cineops-ai-507217
   GOOGLE_CLOUD_LOCATION=us-central1
   CINEOPS_GEMINI_MODEL=gemini-2.5-flash

   # Execution Mode (1 = Offline Mock Mode; 0 = Live Gemini & Parallel)
   CINEOPS_MOCK_MODE=1

   # Parallel Search API Key
   PARALLEL_API_KEY=your_parallel_api_key_here
   ```

---

## 11. Running the Application

Launch the FastAPI application server locally using Uvicorn:

```powershell
.venv\Scripts\python.exe -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

### Access Points
* **Web Command Center**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Interactive API Docs (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **API Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### User Journeys

#### Text Screenplay Flow:
1. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
2. Click **"Load Sample Script"** (or paste custom text).
3. Click **"Analyze Screenplay & Build Plan"**.

#### PDF Screenplay Flow:
1. Drag and drop a `.pdf` file into the PDF upload dropzone.
2. Click **"Analyze PDF Screenplay"**.

---

## 12. Testing

CineOps AI includes a test suite with 100% offline mock execution mode.

Run the test suite:

```powershell
.venv\Scripts\python.exe -m pytest tests/ -v
```

### Verification Result
```text
======================= 27 passed in 3.28s =======================
```
* **Test Count**: 27 passed unit tests.
* **Network Isolation**: Zero external API calls occur during mock mode tests.

---

## 13. Security

* **Git Exclusion**: `.env` and `.venv` are strictly ignored via `.gitignore`.
* **Environment Variable Storage**: All credentials (`PARALLEL_API_KEY`, Google Cloud settings) are loaded exclusively via environment variables.
* **Zero Credential Exposure**: API keys are never returned in REST responses or logged to console outputs.
* **Mock Safeguard**: Default mock mode prevents unintended API billing during development.

---

## 14. Hackathon Requirement Mapping

| Requirement | CineOps AI Implementation |
| :--- | :--- |
| **Gemini / Google Cloud** | Built on Google ADK, Google GenAI SDK, and Vertex AI (`gemini-2.5-flash`). |
| **Agentic Workflow** | Multi-agent collaboration between Screenplay Analyst Agent & Production Planner Agent. |
| **Partner Integration** | Official Parallel Search API (`parallel-web` SDK) for film set safety research. |
| **Real Media Workflow** | Converts raw screenplay PDFs into structured film production plans. |
| **Web Dashboard** | Single-page command center UI served via FastAPI. |
| **Open Source Repository** | Clean, documented codebase with comprehensive pytest suite. |

---

## 15. Why This Is Agentic

CineOps AI goes beyond basic LLM prompts or simple wrappers:

1. **Multi-Agent Decomposition**: Separates creative screenplay analysis from logistically constrained production planning.
2. **Autonomous Tool Usage**: Agents determine when external information (such as electrical codes or drone permits) is required and trigger Parallel Search API calls.
3. **Structured State Synthesis**: Outputs are governed by strict Pydantic schemas, ensuring structured data flow between agents.
4. **Algorithmic Grouping & Reasoning**: Synthesizes scene parameters into optimal shooting units and safety mitigation plans based on logical constraints.

---

## 16. Demo Walkthrough

1. Open the **CineOps AI Dashboard** at `http://127.0.0.1:8000/`.
2. Click **"Load Sample Script"** (or drag & drop a screenplay PDF).
3. Click **"Analyze Screenplay & Build Plan"**.
4. Observe the **3-stage progress modal** (*Analyst Agent ➔ Parallel Research ➔ Production Planner*).
5. Review the **Screenplay Breakdown** tab with filterable scene cards (INT/EXT, Night).
6. Explore the **Production Plan** dashboard:
   - **Shooting Schedule**: Day-by-day scene allocations and hours.
   - **Location Units**: Groupings minimizing physical unit moves.
   - **Resource Matrix**: Gear, stunt equipment, and lighting needs.
   - **Risk Management Matrix**: Categorized hazards and mitigation protocols.
   - **Parallel Research Hub**: Live web search citations and safety guidelines.

---

## 17. Current Status & Roadmap

### Completed Features
* Screenplay text parsing & 11-parameter scene extraction
* PDF screenplay file ingestion (`pypdf`)
* Official Parallel Search API integration
* Production Planner agentic workflow
* FastAPI backend API with Pydantic validation
* Dark cinematic web command center UI
* 27 automated unit tests

### Pending Work
* Live Gemini API execution upon Google Cloud billing activation
* Google Cloud Run container deployment
* Final hackathon demo video recording

---

## 18. License

This project is open-source and licensed under the **[MIT License](LICENSE)**. See the `LICENSE` file in the repository root for full details.

---

## 19. Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request on the [GitHub Repository](https://github.com/aastha-yadav2/CineopsAI).

---

## 20. Acknowledgements

* **Google Cloud & Vertex AI**: For agentic LLM infrastructure.
* **Google ADK & GenAI SDK**: For agent orchestration frameworks.
* **Parallel**: For real-time web search capabilities.
* **FastAPI & Pydantic**: For backend API infrastructure.
