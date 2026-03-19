"""
Tools for ai-code-refactorer recipe.
Uses CodeAgent for intelligent code refactoring.
"""

from praisonaiagents import CodeAgent
from praisonaiagents.tools import read_file, write_file

_code_agent = None

def _get_code_agent():
    global _code_agent
    if _code_agent is None:
        _code_agent = CodeAgent()
    return _code_agent


def refactor_code(code: str, instructions: str = "", language: str = "python") -> str:
    """
    Refactor code to improve quality.
    
    Args:
        code: Code to refactor
        instructions: Specific refactoring instructions
        language: Programming language
        
    Returns:
        Refactored code
    """
    agent = _get_code_agent()
    return agent.refactor(code, instructions=instructions, language=language)


def read_source_file(file_path: str) -> str:
    """
    Read source code from a file.
    
    Args:
        file_path: Path to source file
        
    Returns:
        Source code content
    """
    return read_file(file_path)


def fix_bugs(code: str, error: str = "", language: str = "python") -> str:
    """
    Fix bugs in code.
    
    Args:
        code: Code with bugs
        error: Error message or bug description
        language: Programming language
        
    Returns:
        Fixed code
    """
    agent = _get_code_agent()
    return agent.fix(code, error=error, language=language)


def optimize_performance(code: str, language: str = "python") -> str:
    """
    Optimize code for better performance.
    
    Args:
        code: Code to optimize
        language: Programming language
        
    Returns:
        Optimized code
    """
    agent = _get_code_agent()
    return agent.refactor(
        code,
        instructions="Optimize this code for better performance. Focus on: time complexity, memory usage, and efficiency.",
        language=language
    )


def modernize_code(code: str, language: str = "python") -> str:
    """
    Update code to use modern language features.
    
    Args:
        code: Code to modernize
        language: Programming language
        
    Returns:
        Modernized code
    """
    agent = _get_code_agent()
    return agent.refactor(
        code,
        instructions="Modernize this code to use current best practices and modern language features.",
        language=language
    )


def save_refactored(code: str, output_path: str) -> str:
    """
    Save refactored code to file.
    
    Args:
        code: Refactored code
        output_path: Output file path
        
    Returns:
        Path to saved file
    """
    write_file(output_path, code)
    return output_path


TOOLS = [read_source_file, refactor_code, fix_bugs, optimize_performance, modernize_code, save_refactored]


def get_all_tools():
    return TOOLS
