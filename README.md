<<<<<<< HEAD
# CineopsAI
=======
# CineOps AI - Foundation Setup

Autonomous film-production assistant for the Google Cloud Agentic Cinema Hackathon.

## Prerequisites

- Python 3.10+
- Google Cloud SDK (`gcloud`)

## Authentication Setup (Google Cloud Vertex AI)

This project uses Google Cloud / Vertex AI authentication (`google.auth.default()`).

1. Authenticate Application Default Credentials (ADC) on your machine:
   ```bash
   gcloud auth application-default login
   ```
2. Verify that your `.env` contains:
   ```env
   GOOGLE_GENAI_USE_VERTEXAI=TRUE
   GOOGLE_CLOUD_PROJECT=cineops-ai-507217
   GOOGLE_CLOUD_LOCATION=us-central1
   ```

## Installation

1. Activate the Python virtual environment:
   - **Windows PowerShell**:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS**:
     ```bash
     source .venv/bin/activate
     ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Minimal Test Agent

To run the test agent (`cineops_agent`) with Google ADK and Gemini via Vertex AI:

```bash
python -m src.main
```

### Environment Configuration & Secrets
All configurations are managed strictly via environment variables loaded from `.env` using `python-dotenv`. Secrets and credentials are never hardcoded.
>>>>>>> 23c1438 (Initial commit: CineOps AI Screenplay Production Assistant & Web Dashboard)
