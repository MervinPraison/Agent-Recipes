# Newsletter Generator

Generate email newsletters from content

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-newsletter-generator <input>

# With output directory
praison recipes run ai-newsletter-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-newsletter-generator <input> --dry-run

# Show recipe info
praison recipes info ai-newsletter-generator

# Check dependencies
praison recipes doctor ai-newsletter-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-newsletter-generator")
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

`web`, `newsletter`, `email`

## License

Apache-2.0
