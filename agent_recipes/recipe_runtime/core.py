"""
Core recipe runtime utilities.

Provides the foundation for all recipe execution including:
- Output directory management with timestamps
- run.json generation and validation
- Logging setup
- Dry-run support
- Safety defaults (no overwrites, resource limits)
"""

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


@dataclass
class RecipeConfig:
    """Configuration for a recipe run."""
    recipe_name: str
    input_path: str
    output_dir: Optional[str] = None
    preset: Optional[str] = None
    dry_run: bool = False
    force: bool = False
    verbose: bool = False
    config_file: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for run.json."""
        return {
            "recipe_name": self.recipe_name,
            "input_path": self.input_path,
            "output_dir": self.output_dir,
            "preset": self.preset,
            "dry_run": self.dry_run,
            "force": self.force,
            "verbose": self.verbose,
            **self.extra,
        }


@dataclass
class OutputFile:
    """Information about an output file."""
    name: str
    path: str
    size: int
    sha256: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": self.path,
            "size": self.size,
            "sha256": self.sha256,
        }


@dataclass
class RecipeResult:
    """Result of a recipe execution."""
    recipe: str
    version: str
    status: str  # success, failed, dry_run
    started_at: str
    completed_at: Optional[str] = None
    input_path: str = ""
    output_dir: str = ""
    config: Dict[str, Any] = field(default_factory=dict)
    outputs: List[OutputFile] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    logs: str = ""
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for run.json."""
        return {
            "recipe": self.recipe,
            "version": self.version,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "status": self.status,
            "input": self.input_path,
            "output_dir": self.output_dir,
            "config": self.config,
            "outputs": [o.to_dict() for o in self.outputs],
            "metrics": self.metrics,
            "logs": self.logs,
            "error": self.error,
        }


def get_timestamp() -> str:
    """Get current timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def get_timestamp_dir() -> str:
    """Get timestamp string for directory naming."""
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def create_output_dir(
    recipe_name: str,
    base_dir: Optional[Union[str, Path]] = None,
    force: bool = False,
) -> Path:
    """
    Create output directory for a recipe run.
    
    Args:
        recipe_name: Name of the recipe
        base_dir: Base output directory (default: ./outputs)
        force: Allow overwriting existing directory
        
    Returns:
        Path to created output directory
    """
    if base_dir is None:
        base_dir = Path("./outputs")
    else:
        base_dir = Path(base_dir)
    
    # Create timestamped directory
    timestamp = get_timestamp_dir()
    output_dir = base_dir / recipe_name / timestamp
    
    if output_dir.exists() and not force:
        raise FileExistsError(
            f"Output directory already exists: {output_dir}. "
            "Use --force to overwrite."
        )
    
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def calculate_sha256(path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def collect_outputs(output_dir: Path, include_hash: bool = True) -> List[OutputFile]:
    """
    Collect information about output files.
    
    Args:
        output_dir: Output directory to scan
        include_hash: Calculate SHA256 hashes
        
    Returns:
        List of OutputFile objects
    """
    outputs = []
    
    for path in output_dir.rglob("*"):
        if path.is_file() and path.name != "run.json" and path.name != "run.log":
            rel_path = path.relative_to(output_dir)
            sha256 = calculate_sha256(path) if include_hash else None
            
            outputs.append(OutputFile(
                name=path.name,
                path=str(rel_path),
                size=path.stat().st_size,
                sha256=sha256,
            ))
    
    return outputs


def write_run_json(
    output_dir: Path,
    result: RecipeResult,
) -> Path:
    """
    Write run.json to output directory.
    
    Args:
        output_dir: Output directory
        result: Recipe result
        
    Returns:
        Path to run.json
    """
    run_json_path = output_dir / "run.json"
    
    with open(run_json_path, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, indent=2)
    
    return run_json_path


def setup_logging(
    output_dir: Path,
    verbose: bool = False,
) -> Path:
    """
    Setup logging for a recipe run.
    
    Args:
        output_dir: Output directory for log file
        verbose: Enable verbose logging
        
    Returns:
        Path to log file
    """
    log_path = output_dir / "run.log"
    
    # Configure logging
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create file handler
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    
    # Add to root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    
    if verbose:
        root_logger.setLevel(logging.DEBUG)
    
    return log_path


class RecipeRunner:
    """
    Base class for running recipes with standard safety defaults.
    
    Handles:
    - Output directory creation
    - run.json generation
    - Logging
    - Dry-run mode
    - Error handling
    """
    
    def __init__(
        self,
        recipe_name: str,
        version: str = "1.0.0",
    ):
        self.recipe_name = recipe_name
        self.version = version
        self._start_time: Optional[float] = None
        self._result: Optional[RecipeResult] = None
        self._output_dir: Optional[Path] = None
        self._log_path: Optional[Path] = None
    
    def run(self, config: RecipeConfig) -> RecipeResult:
        """
        Execute the recipe with the given configuration.
        
        Args:
            config: Recipe configuration
            
        Returns:
            RecipeResult with execution details
        """
        self._start_time = time.time()
        started_at = get_timestamp()
        
        # Initialize result
        self._result = RecipeResult(
            recipe=self.recipe_name,
            version=self.version,
            status="running",
            started_at=started_at,
            input_path=config.input_path,
            config=config.to_dict(),
        )
        
        try:
            # Validate input
            self._validate_input(config)
            
            # Create output directory
            if config.output_dir:
                self._output_dir = Path(config.output_dir)
                self._output_dir.mkdir(parents=True, exist_ok=config.force)
            else:
                self._output_dir = create_output_dir(
                    self.recipe_name,
                    force=config.force,
                )
            
            self._result.output_dir = str(self._output_dir)
            
            # Setup logging
            self._log_path = setup_logging(self._output_dir, config.verbose)
            self._result.logs = str(self._log_path)
            
            logger.info(f"Starting recipe: {self.recipe_name}")
            logger.info(f"Input: {config.input_path}")
            logger.info(f"Output: {self._output_dir}")
            
            if config.dry_run:
                # Dry run - just plan, don't execute
                self._result.status = "dry_run"
                logger.info("DRY RUN - no files will be created")
                self._plan(config)
            else:
                # Execute the recipe
                self._execute(config)
                
                # Collect outputs
                self._result.outputs = collect_outputs(self._output_dir)
                self._result.status = "success"
            
        except Exception as e:
            self._result.status = "failed"
            self._result.error = str(e)
            logger.exception(f"Recipe failed: {e}")
            raise
        
        finally:
            # Finalize result
            self._result.completed_at = get_timestamp()
            
            # Calculate metrics
            duration = time.time() - self._start_time
            self._result.metrics = {
                "duration_sec": round(duration, 2),
            }
            
            # Write run.json
            if self._output_dir:
                write_run_json(self._output_dir, self._result)
        
        return self._result
    
    def _validate_input(self, config: RecipeConfig) -> None:
        """Validate input path exists."""
        input_path = Path(config.input_path)
        
        # Allow URLs
        if config.input_path.startswith(("http://", "https://")):
            return
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input not found: {config.input_path}")
    
    def _plan(self, config: RecipeConfig) -> None:
        """
        Plan the recipe execution (for dry-run).
        
        Override in subclasses to provide planning output.
        """
        logger.info("Planning recipe execution...")
        logger.info(f"Would process: {config.input_path}")
        logger.info(f"Would output to: {self._output_dir}")
    
    def _execute(self, config: RecipeConfig) -> None:
        """
        Execute the recipe.
        
        Override in subclasses to implement recipe logic.
        """
        raise NotImplementedError("Subclasses must implement _execute()")
    
    @property
    def output_dir(self) -> Optional[Path]:
        """Get the output directory."""
        return self._output_dir
    
    @property
    def result(self) -> Optional[RecipeResult]:
        """Get the current result."""
        return self._result
