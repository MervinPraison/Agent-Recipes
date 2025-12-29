# Slide Generator

Generate presentation slides from text/outline

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-slide-generator <input>

# With output directory
praison recipes run ai-slide-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-slide-generator <input> --dry-run

# Show recipe info
praison recipes info ai-slide-generator

# Check dependencies
praison recipes doctor ai-slide-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-slide-generator")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai
- python-pptx

### Environment Variables
- OPENAI_API_KEY

### External Tools
- None

## Tags

`document`, `presentation`, `slides`

## License

Apache-2.0
