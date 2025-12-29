# Blog Generator

Generate SEO-optimized blog posts

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-blog-generator <input>

# With output directory
praison recipes run ai-blog-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-blog-generator <input> --dry-run

# Show recipe info
praison recipes info ai-blog-generator

# Check dependencies
praison recipes doctor ai-blog-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-blog-generator")
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

`web`, `blog`, `content`

## License

Apache-2.0
