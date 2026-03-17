"""
Repository parser utility for extracting and parsing code from repositories.
"""
import os
import ast
from typing import Optional, Dict, List
from pathlib import Path


class RepoParser:
    """Utility class for parsing repository code."""
    
    SUPPORTED_EXTENSIONS = {
        '.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs',
        '.rb', '.php', '.swift', '.kt', '.cs', '.html', '.css'
    }
    
    def __init__(self):
        """Initialize repository parser."""
        self.max_file_size = 1024 * 1024  # 1MB limit per file
    
    def parse_repository(self, repo_path: str) -> str:
        """
        Parse entire repository and extract code content.
        
        Args:
            repo_path: Path to the repository
            
        Returns:
            Combined code content from all supported files
        """
        if not os.path.exists(repo_path):
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        code_contents = []
        repo_path_obj = Path(repo_path)
        
        for file_path in repo_path_obj.rglob("*"):
            if file_path.is_file() and file_path.suffix in self.SUPPORTED_EXTENSIONS:
                # Skip common directories
                if any(skip in str(file_path) for skip in ['node_modules', '.git', '__pycache__', '.venv', 'venv']):
                    continue
                
                try:
                    content = self._read_file(file_path)
                    if content:
                        code_contents.append(f"\n# File: {file_path.relative_to(repo_path_obj)}\n{content}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue
        
        return "\n".join(code_contents)
    
    def parse_files(self, file_paths: List[str]) -> str:
        """
        Parse specific files and extract code content.
        
        Args:
            file_paths: List of file paths to parse
            
        Returns:
            Combined code content from specified files
        """
        code_contents = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue
            
            try:
                content = self._read_file(Path(file_path))
                if content:
                    code_contents.append(f"\n# File: {file_path}\n{content}")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue
        
        return "\n".join(code_contents)
    
    def parse_code_content(self, content: str, filename: str) -> Dict:
        """
        Parse code content and extract metadata.
        
        Args:
            content: Code content string
            filename: Name of the file
            
        Returns:
            Dictionary with parsed code information
        """
        file_ext = Path(filename).suffix
        language = self._detect_language(file_ext)
        
        parsed_info = {
            "filename": filename,
            "language": language,
            "content": content,
            "lines": len(content.split('\n')),
            "size": len(content)
        }
        
        # Add language-specific parsing if needed
        if language == "python":
            parsed_info["functions"] = self._extract_python_functions(content)
        
        return parsed_info
    
    def _read_file(self, file_path: Path) -> Optional[str]:
        """
        Read file content safely.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File content or None if error
        """
        try:
            if file_path.stat().st_size > self.max_file_size:
                print(f"File too large, skipping: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    
    def _detect_language(self, extension: str) -> str:
        """
        Detect programming language from file extension.
        
        Args:
            extension: File extension
            
        Returns:
            Language name
        """
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.cs': 'csharp'
        }
        return language_map.get(extension, 'unknown')
    
    def _extract_python_functions(self, content: str) -> List[str]:
        """
        Extract function names from Python code.
        
        Args:
            content: Python code content
            
        Returns:
            List of function names
        """
        try:
            tree = ast.parse(content)
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
            return functions
        except Exception:
            return []
    
    def check_status(self) -> str:
        """Check if parser is operational."""
        return "operational"

