# Note Summarizer

Summarize notes and documents

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-note-summarizer <input>

# With output directory
praison recipes run ai-note-summarizer <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-note-summarizer <input> --dry-run

# Show recipe info
praison recipes info ai-note-summarizer

# Check dependencies
praison recipes doctor ai-note-summarizer
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-note-summarizer")
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

`productivity`, `notes`, `summary`

## License

Apache-2.0
