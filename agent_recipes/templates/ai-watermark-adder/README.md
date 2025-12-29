# Watermark Adder

Batch add watermarks/logos to images

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-watermark-adder <input>

# With output directory
praison recipes run ai-watermark-adder <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-watermark-adder <input> --dry-run

# Show recipe info
praison recipes info ai-watermark-adder

# Check dependencies
praison recipes doctor ai-watermark-adder
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-watermark-adder")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- pillow

### Environment Variables
- None

### External Tools
- None

## Tags

`image`, `watermark`, `branding`

## License

Apache-2.0
