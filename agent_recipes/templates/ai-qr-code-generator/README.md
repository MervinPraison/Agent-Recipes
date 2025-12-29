# Qr Code Generator

Generate QR codes from data

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-qr-code-generator <input>

# With output directory
praison recipes run ai-qr-code-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-qr-code-generator <input> --dry-run

# Show recipe info
praison recipes info ai-qr-code-generator

# Check dependencies
praison recipes doctor ai-qr-code-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-qr-code-generator")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- qrcode
- pillow

### Environment Variables
- None

### External Tools
- None

## Tags

`productivity`, `qr-code`, `generation`

## License

Apache-2.0
