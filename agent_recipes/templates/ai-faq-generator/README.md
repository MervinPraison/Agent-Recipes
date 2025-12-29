# Faq Generator

Generate FAQ from documentation/knowledge base

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-faq-generator <input>

# With output directory
praison recipes run ai-faq-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-faq-generator <input> --dry-run

# Show recipe info
praison recipes info ai-faq-generator

# Check dependencies
praison recipes doctor ai-faq-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-faq-generator")
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

`document`, `faq`, `generation`

## License

Apache-2.0
