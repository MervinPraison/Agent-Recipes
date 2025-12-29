# Code Refactorer

Refactor code with AI suggestions (patch-based, tests-first option)

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-code-refactorer <input>

# With output directory
praison recipes run ai-code-refactorer <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-code-refactorer <input> --dry-run

# Show recipe info
praison recipes info ai-code-refactorer

# Check dependencies
praison recipes doctor ai-code-refactorer
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-code-refactorer")
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

`code`, `refactoring`, `improvement`

## License

Apache-2.0
