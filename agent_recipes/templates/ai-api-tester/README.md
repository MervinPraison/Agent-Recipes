# Api Tester

Auto-generate and run API endpoint tests

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-api-tester <input>

# With output directory
praison recipes run ai-api-tester <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-api-tester <input> --dry-run

# Show recipe info
praison recipes info ai-api-tester

# Check dependencies
praison recipes doctor ai-api-tester
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-api-tester")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai
- requests

### Environment Variables
- OPENAI_API_KEY

### External Tools
- None

## Tags

`code`, `api`, `testing`

## License

Apache-2.0
