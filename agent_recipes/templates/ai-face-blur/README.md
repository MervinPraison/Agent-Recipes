# Face Blur

Detect and blur faces for privacy protection

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-face-blur <input>

# With output directory
praison recipes run ai-face-blur <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-face-blur <input> --dry-run

# Show recipe info
praison recipes info ai-face-blur

# Check dependencies
praison recipes doctor ai-face-blur
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-face-blur")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- opencv-python
- pillow

### Environment Variables
- None

### External Tools
- None

## Tags

`image`, `privacy`, `face`, `blur`

## License

Apache-2.0
