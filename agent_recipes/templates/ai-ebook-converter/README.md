# Ebook Converter

Convert documents to EPUB/MOBI with formatting

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-ebook-converter <input>

# With output directory
praison recipes run ai-ebook-converter <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-ebook-converter <input> --dry-run

# Show recipe info
praison recipes info ai-ebook-converter

# Check dependencies
praison recipes doctor ai-ebook-converter
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-ebook-converter")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- None

### Environment Variables
- None

### External Tools
- pandoc
- calibre

## Tags

`document`, `ebook`, `conversion`

## License

Apache-2.0
