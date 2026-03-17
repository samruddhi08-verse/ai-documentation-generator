"""
AI service for generating documentation using AI models.
"""
import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class AIService:
    """Service for AI-powered documentation generation."""
    
    def __init__(self):
        """Initialize AI service with API key."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("AI_MODEL", "gpt-4")
    
    async def generate_documentation(
        self,
        code_content: str,
        doc_type: str = "api",
        language: Optional[str] = None
    ) -> str:
        """
        Generate documentation for given code content.
        
        Args:
            code_content: The code content to document
            doc_type: Type of documentation (api, readme, code_comments, etc.)
            language: Programming language of the code
            
        Returns:
            Generated documentation string
        """
        prompt = self._build_prompt(code_content, doc_type, language)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert technical documentation writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating documentation: {str(e)}")
    
    def _build_prompt(
        self,
        code_content: str,
        doc_type: str,
        language: Optional[str] = None
    ) -> str:
        """
        Build the prompt for AI documentation generation.
        
        Args:
            code_content: Code content to document
            doc_type: Type of documentation
            language: Programming language
            
        Returns:
            Formatted prompt string
        """
        doc_type_instructions = {
            "api": "Generate comprehensive API documentation including endpoints, parameters, responses, and examples.",
            "readme": "Generate a README.md file with project description, installation instructions, usage examples, and features.",
            "code_comments": "Add detailed inline comments explaining the code logic, parameters, and return values.",
            "technical": "Generate technical documentation with architecture overview, design decisions, and implementation details."
        }
        
        instruction = doc_type_instructions.get(doc_type, doc_type_instructions["api"])
        lang_note = f" The code is written in {language}." if language else ""
        
        prompt = f"""
        {instruction}{lang_note}
        
        Code content:
        {code_content}
        
        Please generate well-structured, clear, and comprehensive documentation.
        """
        
        return prompt
    
    def check_status(self) -> str:
        """Check if AI service is operational."""
        try:
            # Simple check - could be enhanced with actual API health check
            return "operational" if self.client else "unavailable"
        except Exception:
            return "unavailable"

