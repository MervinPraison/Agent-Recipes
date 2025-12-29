# Background Music Generator

Generate royalty-free background music for videos

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-background-music-generator <input>

# With output directory
praison recipes run ai-background-music-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-background-music-generator <input> --dry-run

# Show recipe info
praison recipes info ai-background-music-generator

# Check dependencies
praison recipes doctor ai-background-music-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-background-music-generator")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai

### Environment Variables
- OPENAI_API_KEY

### External Tools
- None

## Tags

`audio`, `music`, `generation`

## License

Apache-2.0
