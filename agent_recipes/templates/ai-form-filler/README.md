# Form Filler

Auto-fill PDF forms from data sources

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-form-filler <input>

# With output directory
praison recipes run ai-form-filler <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-form-filler <input> --dry-run

# Show recipe info
praison recipes info ai-form-filler

# Check dependencies
praison recipes doctor ai-form-filler
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-form-filler")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- pypdf
- openai

### Environment Variables
- OPENAI_API_KEY

### External Tools
- None

## Tags

`document`, `pdf`, `forms`

## License

Apache-2.0
