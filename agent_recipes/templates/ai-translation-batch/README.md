# Translation Batch

Batch translate documents to multiple languages

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-translation-batch <input>

# With output directory
praison recipes run ai-translation-batch <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-translation-batch <input> --dry-run

# Show recipe info
praison recipes info ai-translation-batch

# Check dependencies
praison recipes doctor ai-translation-batch
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-translation-batch")
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

`productivity`, `translation`, `localization`

## License

Apache-2.0
