# Video Compressor

AI-optimized video compression maintaining quality with presets

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-video-compressor <input>

# With output directory
praison recipes run ai-video-compressor <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-video-compressor <input> --dry-run

# Show recipe info
praison recipes info ai-video-compressor

# Check dependencies
praison recipes doctor ai-video-compressor
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-video-compressor")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- ffmpeg-python

### Environment Variables
- None

### External Tools
- ffmpeg

## Tags

`video`, `compression`, `optimization`

## License

Apache-2.0
