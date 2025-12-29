# Log Analyzer

Analyze logs for anomalies/patterns

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-log-analyzer <input>

# With output directory
praison recipes run ai-log-analyzer <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-log-analyzer <input> --dry-run

# Show recipe info
praison recipes info ai-log-analyzer

# Check dependencies
praison recipes doctor ai-log-analyzer
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-log-analyzer")
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

`data`, `logs`, `analysis`

## License

Apache-2.0
