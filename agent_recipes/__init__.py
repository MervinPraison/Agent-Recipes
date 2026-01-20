"""
Agent Recipes - Real-world AI agent templates for PraisonAI

This package provides ready-to-use templates for common AI agent workflows.
"""

__version__ = "0.1.0"
__all__ = ["get_template_path", "list_templates", "run_recipe", "call_recipe"]

from pathlib import Path
from typing import Any, Dict, Optional


def get_template_path(template_name: str) -> Path:
    """Get the path to a template directory."""
    templates_dir = Path(__file__).parent / "templates"
    template_path = templates_dir / template_name
    if not template_path.exists():
        raise ValueError(f"Template not found: {template_name}")
    return template_path


def list_templates() -> list:
    """List all available templates."""
    templates_dir = Path(__file__).parent / "templates"
    if not templates_dir.exists():
        return []
    return [d.name for d in templates_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]


def run_recipe(
    recipe_name: str,
    input_data: Optional[str] = None,
    variables: Optional[Dict[str, Any]] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Run a recipe and return the result.
    
    This is the main entry point for programmatically executing recipes.
    It finds the recipe, loads its tools, and executes the workflow.
    
    Args:
        recipe_name: Name of the recipe template (e.g., "wordpress-publisher")
        input_data: Input string to pass to the workflow
        variables: Additional variables to merge with workflow variables
        verbose: Enable verbose output
        
    Returns:
        Dict with 'output' key containing the workflow result
        
    Example:
        from agent_recipes import run_recipe
        
        result = run_recipe(
            "wordpress-publisher",
            input_data="ARTICLE_TITLE: Test\\nARTICLE_CONTENT: ..."
        )
        print(result['output'])
    """
    # Lazy import to avoid circular dependencies
    from praisonaiagents.workflows import WorkflowManager
    import importlib.util
    import sys
    
    # Get recipe path
    recipe_path = get_template_path(recipe_name)
    agents_yaml = recipe_path / "agents.yaml"
    
    if not agents_yaml.exists():
        raise ValueError(f"Recipe {recipe_name} does not have agents.yaml")
    
    # Load tools from recipe's tools.py if it exists
    tool_registry = {}
    tools_py = recipe_path / "tools.py"
    if tools_py.exists():
        # Dynamically import the tools module
        spec = importlib.util.spec_from_file_location(f"{recipe_name}_tools", tools_py)
        tools_module = importlib.util.module_from_spec(spec)
        sys.modules[f"{recipe_name}_tools"] = tools_module
        spec.loader.exec_module(tools_module)
        
        # Get tools from the module's TOOLS dict or get_all_tools function
        if hasattr(tools_module, 'TOOLS'):
            tool_registry = tools_module.TOOLS
        elif hasattr(tools_module, 'get_all_tools'):
            for tool in tools_module.get_all_tools():
                tool_registry[tool.__name__] = tool
    
    # Execute the workflow
    manager = WorkflowManager()
    result = manager.execute_yaml(
        agents_yaml,
        input_data=input_data,
        variables=variables or {},
        tool_registry=tool_registry,
        verbose=verbose
    )
    
    return result


def call_recipe(recipe_name: str, input_data: str = "") -> str:
    """
    Call another recipe from within an agent.
    
    This is a tool function that agents can use to invoke other recipes
    and get their output.
    
    Args:
        recipe_name: Name of the recipe to call (e.g., "wordpress-publisher")
        input_data: Input string to pass to the recipe
        
    Returns:
        The output from the called recipe as a string
        
    Example:
        # In an agent's tool list:
        from agent_recipes import call_recipe
        
        agent = Agent(
            name="Orchestrator",
            tools=[call_recipe]
        )
        
        # The agent can then call:
        # call_recipe("wordpress-publisher", "ARTICLE_TITLE: Test\\nARTICLE_CONTENT: ...")
    """
    try:
        result = run_recipe(
            recipe_name=recipe_name,
            input_data=input_data,
            verbose=False
        )
        return str(result.get("output", ""))
    except Exception as e:
        return f"Error calling recipe {recipe_name}: {e}"
