# Product Description Generator

Generate e-commerce product descriptions

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-product-description-generator <input>

# With output directory
praison recipes run ai-product-description-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-product-description-generator <input> --dry-run

# Show recipe info
praison recipes info ai-product-description-generator

# Check dependencies
praison recipes doctor ai-product-description-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-product-description-generator")
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

`web`, `ecommerce`, `product`

## License

Apache-2.0
