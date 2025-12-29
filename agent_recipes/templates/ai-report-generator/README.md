# Report Generator

Generate business reports from data

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-report-generator <input>

# With output directory
praison recipes run ai-report-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-report-generator <input> --dry-run

# Show recipe info
praison recipes info ai-report-generator

# Check dependencies
praison recipes doctor ai-report-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-report-generator")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai
- pandas
- matplotlib

### Environment Variables
- OPENAI_API_KEY

### External Tools
- None

## Tags

`data`, `report`, `analytics`

## License

Apache-2.0
