# Email Parser

Extract structured data from emails

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-email-parser <input>

# With output directory
praison recipes run ai-email-parser <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-email-parser <input> --dry-run

# Show recipe info
praison recipes info ai-email-parser

# Check dependencies
praison recipes doctor ai-email-parser
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-email-parser")
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

`productivity`, `email`, `extraction`

## License

Apache-2.0
