"""
Tools for ai-code-documenter recipe.
Uses CodeAgent for code explanation and documentation generation.
"""

from praisonaiagents import CodeAgent
from praisonaiagents.tools import read_file, write_file

_code_agent = None

def _get_code_agent():
    global _code_agent
    if _code_agent is None:
        _code_agent = CodeAgent()
    return _code_agent


def read_source_file(file_path: str) -> str:
    """
    Read source code from a file.
    
    Args:
        file_path: Path to source file
        
    Returns:
        Source code content
    """
    return read_file(file_path)


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


def generate_docstrings(code: str, language: str = "python") -> str:
    """
    Generate docstrings for functions/classes in code.
    
    Args:
        code: Code to document
        language: Programming language
        
    Returns:
        Code with added docstrings
    """
    agent = _get_code_agent()
    return agent.refactor(
        code, 
        instructions="Add comprehensive docstrings to all functions, classes, and methods. Follow Google style docstrings.",
        language=language
    )


TOOLS = [read_source_file, explain_code, generate_docstrings]


def get_all_tools():
    return TOOLS
