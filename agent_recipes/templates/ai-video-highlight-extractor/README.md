# Video Highlight Extractor

Auto-detect and extract key moments/highlights from long videos

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-video-highlight-extractor <input>

# With output directory
praison recipes run ai-video-highlight-extractor <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-video-highlight-extractor <input> --dry-run

# Show recipe info
praison recipes info ai-video-highlight-extractor

# Check dependencies
praison recipes doctor ai-video-highlight-extractor
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-video-highlight-extractor")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- ffmpeg-python
- openai

### Environment Variables
- OPENAI_API_KEY

### External Tools
- ffmpeg

## Tags

`video`, `highlights`, `extraction`

## License

Apache-2.0
