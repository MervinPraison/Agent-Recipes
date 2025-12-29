# Audio Enhancer

Noise removal, EQ, and loudness normalization for audio

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-audio-enhancer <input>

# With output directory
praison recipes run ai-audio-enhancer <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-audio-enhancer <input> --dry-run

# Show recipe info
praison recipes info ai-audio-enhancer

# Check dependencies
praison recipes doctor ai-audio-enhancer
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-audio-enhancer")
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

`audio`, `enhancement`, `noise-removal`

## License

Apache-2.0
