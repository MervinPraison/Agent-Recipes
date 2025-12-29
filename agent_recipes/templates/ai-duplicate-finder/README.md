# Duplicate Finder

Find and deduplicate similar files

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-duplicate-finder <input>

# With output directory
praison recipes run ai-duplicate-finder <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-duplicate-finder <input> --dry-run

# Show recipe info
praison recipes info ai-duplicate-finder

# Check dependencies
praison recipes doctor ai-duplicate-finder
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-duplicate-finder")
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

`data`, `deduplication`, `files`

## License

Apache-2.0
