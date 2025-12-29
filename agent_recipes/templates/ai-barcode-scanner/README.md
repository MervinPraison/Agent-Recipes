# Barcode Scanner

Extract data from barcodes/QR codes

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-barcode-scanner <input>

# With output directory
praison recipes run ai-barcode-scanner <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-barcode-scanner <input> --dry-run

# Show recipe info
praison recipes info ai-barcode-scanner

# Check dependencies
praison recipes doctor ai-barcode-scanner
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-barcode-scanner")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- pyzbar
- pillow

### Environment Variables
- None

### External Tools
- None

## Tags

`productivity`, `barcode`, `scanning`

## License

Apache-2.0
