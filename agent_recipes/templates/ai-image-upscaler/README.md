# Image Upscaler

AI upscale images 2x-8x with quality preservation

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-image-upscaler <input>

# With output directory
praison recipes run ai-image-upscaler <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-image-upscaler <input> --dry-run

# Show recipe info
praison recipes info ai-image-upscaler

# Check dependencies
praison recipes doctor ai-image-upscaler
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-image-upscaler")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- realesrgan
- pillow

### Environment Variables
- None

### External Tools
- None

## Tags

`image`, `upscale`, `enhancement`

## License

Apache-2.0
