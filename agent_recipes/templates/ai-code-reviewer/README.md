# Code Reviewer

Automated code review with suggestions

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-code-reviewer <input>

# With output directory
praison recipes run ai-code-reviewer <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-code-reviewer <input> --dry-run

# Show recipe info
praison recipes info ai-code-reviewer

# Check dependencies
praison recipes doctor ai-code-reviewer
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-code-reviewer")
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

`code`, `review`, `quality`

## License

Apache-2.0
