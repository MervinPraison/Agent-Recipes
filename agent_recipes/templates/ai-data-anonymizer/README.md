# Data Anonymizer

Anonymize PII in datasets (GDPR/CCPA-oriented)

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-data-anonymizer <input>

# With output directory
praison recipes run ai-data-anonymizer <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-data-anonymizer <input> --dry-run

# Show recipe info
praison recipes info ai-data-anonymizer

# Check dependencies
praison recipes doctor ai-data-anonymizer
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-data-anonymizer")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai
- pandas

### Environment Variables
- OPENAI_API_KEY

### External Tools
- None

## Tags

`data`, `privacy`, `anonymization`, `gdpr`

## License

Apache-2.0
