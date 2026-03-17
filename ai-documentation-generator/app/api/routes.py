"""
API routes for the documentation generator.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional
from pydantic import BaseModel
from app.services.ai_service import AIService
from app.utils.repo_parser import RepoParser

router = APIRouter()

# Initialize services
ai_service = AIService()
repo_parser = RepoParser()


class GenerateDocRequest(BaseModel):
    """Request model for documentation generation."""
    repository_path: Optional[str] = None
    file_paths: Optional[list[str]] = None
    documentation_type: str = "api"  # api, readme, code_comments, etc.
    language: Optional[str] = None


class GenerateDocResponse(BaseModel):
    """Response model for documentation generation."""
    documentation: str
    status: str
    message: str


@router.post("/generate", response_model=GenerateDocResponse)
async def generate_documentation(request: GenerateDocRequest):
    """
    Generate documentation for a repository or specific files.
    
    Args:
        request: GenerateDocRequest containing repository path or file paths
        
    Returns:
        GenerateDocResponse with generated documentation
    """
    try:
        # Parse repository or files
        if request.repository_path:
            code_content = repo_parser.parse_repository(request.repository_path)
        elif request.file_paths:
            code_content = repo_parser.parse_files(request.file_paths)
        else:
            raise HTTPException(
                status_code=400,
                detail="Either repository_path or file_paths must be provided"
            )
        
        # Generate documentation using AI service
        documentation = await ai_service.generate_documentation(
            code_content=code_content,
            doc_type=request.documentation_type,
            language=request.language
        )
        
        return GenerateDocResponse(
            documentation=documentation,
            status="success",
            message="Documentation generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file for documentation generation.
    
    Args:
        file: File to upload
        
    Returns:
        Parsed file content
    """
    try:
        content = await file.read()
        file_content = content.decode("utf-8")
        
        parsed_content = repo_parser.parse_code_content(
            file_content,
            file.filename
        )
        
        return {
            "filename": file.filename,
            "content": parsed_content,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_status():
    """Get API status."""
    return {
        "status": "operational",
        "ai_service": ai_service.check_status(),
        "repo_parser": repo_parser.check_status()
    }

