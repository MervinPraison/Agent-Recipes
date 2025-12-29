# Video Chapter Generator

Generate timestamped chapters with descriptions for YouTube videos

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-video-chapter-generator <input>

# With output directory
praison recipes run ai-video-chapter-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-video-chapter-generator <input> --dry-run

# Show recipe info
praison recipes info ai-video-chapter-generator

# Check dependencies
praison recipes doctor ai-video-chapter-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-video-chapter-generator")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai

### Environment Variables
- OPENAI_API_KEY

### External Tools
- ffmpeg

## Tags

`video`, `chapters`, `youtube`, `timestamps`

## License

Apache-2.0
