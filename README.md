# AI Documentation Generator

AI Documentation Generator is a backend service that turns source code (entire repositories or selected files) into clear, consistent documentation using AI. It’s designed to help teams bootstrap API docs, README drafts, and technical overviews faster—while keeping the output structured and easy to iterate on.

## Features

- **Repository parsing**: Ingest a whole repo (or a list of files) and extract relevant code content for documentation.
- **Documentation generation**: Produce documentation drafts from code using an AI model (e.g., OpenAI).
- **FastAPI backend**: Simple HTTP API with interactive Swagger docs.
- **Extensible architecture**: Clean separation between API routes, services, and utilities to support future growth.

## Tech Stack

- **Python**
- **FastAPI** (API framework)
- **Uvicorn** (ASGI server)
- **Pydantic** (request/response validation)
- **OpenAI SDK** (AI model integration)
- **GitPython** (planned/optional: repo cloning and git operations)

## Setup Instructions

### Prerequisites

- Python 3.10+ recommended
- An OpenAI API key (if you enable AI generation)

### 1) Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2) Install dependencies

```bash
cd ai-documentation-generator
pip install -r requirements.txt
```

### 3) Configure environment variables

Create a `.env` file inside `ai-documentation-generator/` and set:

```bash
OPENAI_API_KEY=your_openai_api_key_here
AI_MODEL=gpt-4
```

### 4) Run the server (Uvicorn)

```bash
cd ai-documentation-generator
uvicorn app.main:app --reload
```

Now open:
- `http://localhost:8000/` (health/root message)
- `http://localhost:8000/docs` (Swagger UI)

## Future Improvements

- **Clone by Git URL**: Accept a GitHub repo URL and clone it server-side (GitPython), rather than requiring a local path.
- **Richer parsing**: Language-aware parsing (ASTs), symbol graphs, and smarter filtering (ignore tests/build outputs by default).
- **Doc templates**: Output to structured templates (README sections, API reference format, ADRs).
- **Streaming + jobs**: Background tasks for large repos, streaming partial output, and a job/status endpoint.
- **Auth & rate limiting**: API keys/JWT, request quotas, and abuse prevention.
- **Persistence**: Store generated docs and metadata (database + caching).

---

Backend code lives in `ai-documentation-generator/`. For API details and backend-specific notes, see `ai-documentation-generator/README.md`.


