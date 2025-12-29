# Resume Parser

Parse CVs/resumes into structured JSON format

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-resume-parser <input>

# With output directory
praison recipes run ai-resume-parser <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-resume-parser <input> --dry-run

# Show recipe info
praison recipes info ai-resume-parser

# Check dependencies
praison recipes doctor ai-resume-parser
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-resume-parser")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai
- pdftotext

### Environment Variables
- OPENAI_API_KEY

### External Tools
- poppler

## Tags

`document`, `resume`, `cv`, `parsing`

## License

Apache-2.0
