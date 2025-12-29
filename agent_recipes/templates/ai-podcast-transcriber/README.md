# Podcast Transcriber

Full podcast transcription with speaker diarization

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-podcast-transcriber <input>

# With output directory
praison recipes run ai-podcast-transcriber <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-podcast-transcriber <input> --dry-run

# Show recipe info
praison recipes info ai-podcast-transcriber

# Check dependencies
praison recipes doctor ai-podcast-transcriber
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-podcast-transcriber")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai

### Environment Variables
- OPENAI_API_KEY

### External Tools
- ffmpeg

## Tags

`audio`, `podcast`, `transcription`, `diarization`

## License

Apache-2.0
