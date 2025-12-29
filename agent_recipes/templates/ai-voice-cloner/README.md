# Voice Cloner

Clone voice from sample for TTS narration (CONSENT REQUIRED)

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-voice-cloner <input>

# With output directory
praison recipes run ai-voice-cloner <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-voice-cloner <input> --dry-run

# Show recipe info
praison recipes info ai-voice-cloner

# Check dependencies
praison recipes doctor ai-voice-cloner
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-voice-cloner")
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

`audio`, `voice`, `tts`, `cloning`

## License

Apache-2.0
