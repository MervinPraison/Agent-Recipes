"""
Tools for ai-test-generator recipe.
Uses CodeAgent for test generation and execution.
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


def generate_tests(code: str, language: str = "python", framework: str = "pytest") -> str:
    """
    Generate unit tests for the given code.
    
    Args:
        code: Source code to test
        language: Programming language
        framework: Test framework (pytest, unittest, jest)
        
    Returns:
        Generated test code
    """
    agent = _get_code_agent()
    prompt = f"""Generate comprehensive unit tests for this {language} code using {framework}.
Include:
- Happy path tests
- Edge case tests  
- Error handling tests
- Mocking where necessary

Code to test:
{code}"""
    
    return agent.generate(prompt, language=language)


def run_tests(test_code: str) -> str:
    """
    Execute generated tests.
    
    Args:
        test_code: Test code to run
        
    Returns:
        Test execution results
    """
    agent = _get_code_agent()
    return agent.execute(test_code, language="python")


def analyze_coverage(source_code: str, test_code: str) -> str:
    """
    Analyze test coverage and suggest missing tests.
    
    Args:
        source_code: Original source code
        test_code: Generated test code
        
    Returns:
        Coverage analysis and suggestions
    """
    agent = _get_code_agent()
    prompt = f"""Analyze test coverage for this code:

SOURCE:
{source_code[:2000]}

TESTS:
{test_code[:2000]}

Identify:
1. Functions/methods not tested
2. Edge cases not covered
3. Error conditions not tested
4. Suggestions for additional tests"""

    return agent.review(prompt)


def save_tests(test_code: str, output_path: str = "test_generated.py") -> str:
    """
    Save generated tests to file.
    
    Args:
        test_code: Generated test code
        output_path: Output file path
        
    Returns:
        Path to saved file
    """
    write_file(output_path, test_code)
    return output_path


TOOLS = [read_source_file, generate_tests, run_tests, analyze_coverage, save_tests]


def get_all_tools():
    return TOOLS
