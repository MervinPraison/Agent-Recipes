# Api Doc Generator

Generate OpenAPI/Swagger docs from code

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-api-doc-generator <input>

# With output directory
praison recipes run ai-api-doc-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-api-doc-generator <input> --dry-run

# Show recipe info
praison recipes info ai-api-doc-generator

# Check dependencies
praison recipes doctor ai-api-doc-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-api-doc-generator")
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

`code`, `api`, `documentation`, `openapi`

## License

Apache-2.0
