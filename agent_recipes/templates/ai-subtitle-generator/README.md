# Subtitle Generator

Auto-generate SRT/VTT subtitles in 60+ languages with timestamps

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-subtitle-generator <input>

# With output directory
praison recipes run ai-subtitle-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-subtitle-generator <input> --dry-run

# Show recipe info
praison recipes info ai-subtitle-generator

# Check dependencies
praison recipes doctor ai-subtitle-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-subtitle-generator")
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

`video`, `audio`, `subtitles`, `transcription`

## License

Apache-2.0
