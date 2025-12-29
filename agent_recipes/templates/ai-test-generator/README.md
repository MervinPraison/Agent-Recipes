# Test Generator

Generate unit/integration tests from code

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-test-generator <input>

# With output directory
praison recipes run ai-test-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-test-generator <input> --dry-run

# Show recipe info
praison recipes info ai-test-generator

# Check dependencies
praison recipes doctor ai-test-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-test-generator")
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

`code`, `testing`, `generation`

## License

Apache-2.0
