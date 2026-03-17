# AI Documentation Generator

A FastAPI-based backend service for generating comprehensive documentation using AI.

## Features

- Generate API documentation from code
- Create README files automatically
- Add code comments and explanations
- Support for multiple programming languages
- Repository-wide or file-specific documentation generation

## Project Structure

```
ai-documentation-generator/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   └── routes.py        # API endpoints and route handlers
│   ├── services/
│   │   └── ai_service.py    # AI service for documentation generation
│   └── utils/
│       └── repo_parser.py   # Repository and code parsing utilities
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
└── .env                    # Environment variables
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in `.env` file

## Configuration

Copy `.env.example` to `.env` and configure:
- `OPENAI_API_KEY`: Your OpenAI API key
- `AI_MODEL`: AI model to use (default: gpt-4)

## Running the Application

To start the FastAPI server, use uvicorn:

```bash
uvicorn app.main:app --reload
```

**Command breakdown:**
- `uvicorn` - ASGI server for running FastAPI applications
- `app.main:app` - Path to the FastAPI app instance (module:variable)
- `--reload` - Enables auto-reload on code changes (useful for development)

The API will be available at `http://localhost:8000`

**Access the API:**
- Root endpoint: `http://localhost:8000/`
- API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative docs (ReDoc): `http://localhost:8000/redoc`

**Test the root endpoint:**
```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "message": "AI Documentation Generator API is running"
}
```

## API Endpoints

- `POST /api/v1/generate` - Generate documentation
- `POST /api/v1/upload` - Upload file for documentation
- `GET /api/v1/status` - Check API status
- `GET /health` - Health check

## Usage Example

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "repository_path": "/path/to/repo",
    "documentation_type": "api",
    "language": "python"
  }'
```

## License

MIT

