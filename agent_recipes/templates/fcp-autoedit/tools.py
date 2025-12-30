"""
FCP AutoEdit Tools for Agent Recipe

These tools provide the interface between the agent workflow and the
FCP tool package in praisonai-tools.
"""

from typing import Optional


def fcp_doctor_tool() -> dict:
    """
    Run health checks for FCP integration.
    
    Returns a dictionary with check results for:
    - macOS environment
    - Final Cut Pro installation
    - CommandPost installation
    - cmdpost CLI availability
    - Watch folder configuration
    - OpenAI API key
    
    Returns:
        dict: Health check results with 'all_passed' boolean and 'checks' list
    """
    try:
        from praisonai_tools.fcp_tool import fcp_doctor
        return fcp_doctor()
    except ImportError:
        return {
            "success": False,
            "error": "FCP tool not installed. Install with: pip install praisonai-tools",
            "all_passed": False,
            "checks": [],
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "all_passed": False,
            "checks": [],
        }


def fcp_autoedit_tool(
    action: str,
    instruction: Optional[str] = None,
    media_paths: Optional[list] = None,
    project_name: str = "AI Generated Project",
    format_preset: str = "1080p25",
    intent_json: Optional[str] = None,
    fcpxml_content: Optional[str] = None,
    watch_folder: Optional[str] = None,
    dry_run: bool = False,
    model: str = "gpt-4o",
) -> dict:
    """
    FCP AutoEdit tool for generating and injecting FCPXML.
    
    Actions:
    - "generate_intent": Generate EditIntent from instruction
    - "generate_fcpxml": Generate FCPXML from EditIntent
    - "inject": Inject FCPXML into Final Cut Pro
    - "full_pipeline": Run the complete pipeline
    
    Args:
        action: The action to perform
        instruction: Natural language editing instruction
        media_paths: List of media file paths
        project_name: Project name
        format_preset: Format preset (e.g., "1080p25")
        intent_json: EditIntent JSON string (for generate_fcpxml)
        fcpxml_content: FCPXML content (for inject)
        watch_folder: Watch folder path
        dry_run: If True, don't inject into FCP
        model: OpenAI model to use
        
    Returns:
        dict: Result with success status and relevant data
    """
    try:
        from praisonai_tools.fcp_tool import fcp_autoedit
        return fcp_autoedit(
            action=action,
            instruction=instruction,
            media_paths=media_paths,
            project_name=project_name,
            format_preset=format_preset,
            intent_json=intent_json,
            fcpxml_content=fcpxml_content,
            watch_folder=watch_folder,
            dry_run=dry_run,
            model=model,
        )
    except ImportError as e:
        return {
            "success": False,
            "error": f"FCP tool not installed. Install with: pip install praisonai-tools. Error: {e}",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
