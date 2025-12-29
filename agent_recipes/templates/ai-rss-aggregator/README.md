# Rss Aggregator

Aggregate and summarize RSS feeds

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-rss-aggregator <input>

# With output directory
praison recipes run ai-rss-aggregator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-rss-aggregator <input> --dry-run

# Show recipe info
praison recipes info ai-rss-aggregator

# Check dependencies
praison recipes doctor ai-rss-aggregator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-rss-aggregator")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai
- feedparser

### Environment Variables
- OPENAI_API_KEY

### External Tools
- None

## Tags

`web`, `rss`, `aggregation`

## License

Apache-2.0
