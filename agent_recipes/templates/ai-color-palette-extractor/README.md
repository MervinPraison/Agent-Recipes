# Color Palette Extractor

Extract dominant colors from images

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-color-palette-extractor <input>

# With output directory
praison recipes run ai-color-palette-extractor <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-color-palette-extractor <input> --dry-run

# Show recipe info
praison recipes info ai-color-palette-extractor

# Check dependencies
praison recipes doctor ai-color-palette-extractor
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-color-palette-extractor")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- pillow
- colorthief

### Environment Variables
- None

### External Tools
- None

## Tags

`image`, `color`, `palette`

## License

Apache-2.0
