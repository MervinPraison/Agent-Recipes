# Sentiment Analyzer

Analyze sentiment in text data

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-sentiment-analyzer <input>

# With output directory
praison recipes run ai-sentiment-analyzer <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-sentiment-analyzer <input> --dry-run

# Show recipe info
praison recipes info ai-sentiment-analyzer

# Check dependencies
praison recipes doctor ai-sentiment-analyzer
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-sentiment-analyzer")
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

`data`, `sentiment`, `nlp`

## License

Apache-2.0
