# Excel Formula Generator

Generate Excel formulas from descriptions

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-excel-formula-generator <input>

# With output directory
praison recipes run ai-excel-formula-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-excel-formula-generator <input> --dry-run

# Show recipe info
praison recipes info ai-excel-formula-generator

# Check dependencies
praison recipes doctor ai-excel-formula-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-excel-formula-generator")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai

### Environment Variables
- OPENAI_API_KEY

### External Tools
- None

## Tags

`data`, `excel`, `formulas`

## License

Apache-2.0
