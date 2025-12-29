# Invoice Processor

Extract data from invoices/receipts with OCR and structured output

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-invoice-processor <input>

# With output directory
praison recipes run ai-invoice-processor <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-invoice-processor <input> --dry-run

# Show recipe info
praison recipes info ai-invoice-processor

# Check dependencies
praison recipes doctor ai-invoice-processor
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-invoice-processor")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai
- pytesseract

### Environment Variables
- OPENAI_API_KEY

### External Tools
- tesseract

## Tags

`document`, `invoice`, `ocr`, `extraction`

## License

Apache-2.0
