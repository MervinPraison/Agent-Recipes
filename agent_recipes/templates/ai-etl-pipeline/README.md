# Etl Pipeline

Transform data between formats with mapping

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-etl-pipeline <input>

# With output directory
praison recipes run ai-etl-pipeline <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-etl-pipeline <input> --dry-run

# Show recipe info
praison recipes info ai-etl-pipeline

# Check dependencies
praison recipes doctor ai-etl-pipeline
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-etl-pipeline")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- pandas
- openai

### Environment Variables
- OPENAI_API_KEY

### External Tools
- None

## Tags

`data`, `etl`, `transformation`

## License

Apache-2.0
