# Chart Generator

Generate charts/visualizations from data

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-chart-generator <input>

# With output directory
praison recipes run ai-chart-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-chart-generator <input> --dry-run

# Show recipe info
praison recipes info ai-chart-generator

# Check dependencies
praison recipes doctor ai-chart-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-chart-generator")
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

`data`, `chart`, `visualization`

## License

Apache-2.0
