# AI WordPress Post Generator

Research AI news and publish Gutenberg-formatted posts to WordPress.

## Flow

```
Search News → Check Duplicates → Deep Research → Write Content → Publish
```

## Installation

```bash
pip install praisonai praisonai-tools praisonaiwp tavily-python
```

## CLI Usage

```bash
# Navigate to template
cd /path/to/Agent-Recipes/agent_recipes/templates/ai-wordpress-post-generator

# Run workflow
praisonai workflow run agents.yaml
```

Or list available templates:

```bash
praisonai templates list
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

recipe = load_recipe("ai-wordpress-post-generator")
result = recipe.run(input="AI news")
print(result)
```

## Requirements

### Packages
- praisonai
- praisonai-tools
- praisonaiwp
- tavily-python

### Environment Variables
- OPENAI_API_KEY
- TAVILY_API_KEY

## Features

- 5-stage pipeline (gather → dedupe → research → write → publish)
- Gutenberg block formatting (tables, headings, lists)
- Semantic duplicate detection
- British English output
- Title validation blocklist

## Tags

`web`, `wordpress`, `content`, `news`, `gutenberg`

## License

Apache-2.0
