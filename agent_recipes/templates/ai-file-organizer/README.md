# File Organizer

Auto-organize files into folders by content

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-file-organizer <input>

# With output directory
praison recipes run ai-file-organizer <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-file-organizer <input> --dry-run

# Show recipe info
praison recipes info ai-file-organizer

# Check dependencies
praison recipes doctor ai-file-organizer
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-file-organizer")
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

`productivity`, `files`, `organization`

## License

Apache-2.0
