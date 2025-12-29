# Meeting Summarizer

Summarize meeting transcripts with action items

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-meeting-summarizer <input>

# With output directory
praison recipes run ai-meeting-summarizer <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-meeting-summarizer <input> --dry-run

# Show recipe info
praison recipes info ai-meeting-summarizer

# Check dependencies
praison recipes doctor ai-meeting-summarizer
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-meeting-summarizer")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai

### Environment Variables
- OPENAI_API_KEY

### External Tools
- ffmpeg

## Tags

`document`, `meeting`, `summary`, `action-items`

## License

Apache-2.0
