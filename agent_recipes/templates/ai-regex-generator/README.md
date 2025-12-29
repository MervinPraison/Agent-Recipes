# Regex Generator

Generate regex patterns from descriptions

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-regex-generator <input>

# With output directory
praison recipes run ai-regex-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-regex-generator <input> --dry-run

# Show recipe info
praison recipes info ai-regex-generator

# Check dependencies
praison recipes doctor ai-regex-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-regex-generator")
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

`code`, `regex`, `patterns`

## License

Apache-2.0
