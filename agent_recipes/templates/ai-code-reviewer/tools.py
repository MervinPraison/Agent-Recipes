"""
Tools for ai-code-reviewer recipe.
Uses CodeAgent for intelligent code review.
"""

from praisonaiagents import CodeAgent
from praisonaiagents.tools import read_file, analyze_code, lint_code

_code_agent = None

def _get_code_agent():
    global _code_agent
    if _code_agent is None:
        _code_agent = CodeAgent()
    return _code_agent


def review_code(code: str, language: str = "python") -> str:
    """
    Review code for issues, bugs, and improvements.
    
    Args:
        code: Code to review
        language: Programming language
        
    Returns:
        Detailed code review with suggestions
    """
    agent = _get_code_agent()
    return agent.review(code, language=language)


def review_file(file_path: str) -> str:
    """
    Review code from a file.
    
    Args:
        file_path: Path to code file
        
    Returns:
        Detailed code review
    """
    code = read_file(file_path)
    # Detect language from extension
    ext = file_path.split('.')[-1]
    lang_map = {'py': 'python', 'js': 'javascript', 'ts': 'typescript', 'go': 'go', 'rs': 'rust'}
    language = lang_map.get(ext, 'python')
    
    agent = _get_code_agent()
    return agent.review(code, language=language)


def explain_code(code: str, language: str = "python") -> str:
    """
    Explain what the code does in plain language.
    
    Args:
        code: Code to explain
        language: Programming language
        
    Returns:
        Plain language explanation
    """
    agent = _get_code_agent()
    return agent.explain(code, language=language)


def check_security(code: str) -> str:
    """
    Check code for security vulnerabilities.
    
    Args:
        code: Code to analyze
        
    Returns:
        Security analysis report
    """
    agent = _get_code_agent()
    return agent.review(code, language="python")  # Review includes security checks


def lint_python(code: str) -> str:
    """
    Run linting on Python code.
    
    Args:
        code: Python code to lint
        
    Returns:
        Linting results
    """
    return lint_code(code)


TOOLS = [read_file, review_code, review_file, explain_code, check_security, lint_python]


def get_all_tools():
    return TOOLS
