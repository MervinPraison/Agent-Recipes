# Commit Message Generator

Generate git commit messages from diffs

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-commit-message-generator <input>

# With output directory
praison recipes run ai-commit-message-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-commit-message-generator <input> --dry-run

# Show recipe info
praison recipes info ai-commit-message-generator

# Check dependencies
praison recipes doctor ai-commit-message-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-commit-message-generator")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai

### Environment Variables
- OPENAI_API_KEY

### External Tools
- git

## Tags

`code`, `git`, `commit`

## License

Apache-2.0
