# Contract Analyzer

Extract key terms, dates, obligations from contracts (LEGAL DISCLAIMER)

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-contract-analyzer <input>

# With output directory
praison recipes run ai-contract-analyzer <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-contract-analyzer <input> --dry-run

# Show recipe info
praison recipes info ai-contract-analyzer

# Check dependencies
praison recipes doctor ai-contract-analyzer
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-contract-analyzer")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai
- pdftotext

### Environment Variables
- OPENAI_API_KEY

### External Tools
- poppler

## Tags

`document`, `contract`, `legal`, `analysis`

## License

Apache-2.0
