# Background Remover

Batch remove backgrounds from images

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-background-remover <input>

# With output directory
praison recipes run ai-background-remover <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-background-remover <input> --dry-run

# Show recipe info
praison recipes info ai-background-remover

# Check dependencies
praison recipes doctor ai-background-remover
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-background-remover")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- rembg
- pillow

### Environment Variables
- None

### External Tools
- None

## Tags

`image`, `background`, `removal`

## License

Apache-2.0
