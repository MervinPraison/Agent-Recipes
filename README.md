# Agent Recipes

Real-world AI agent templates and recipes for PraisonAI.

## Installation

```bash
pip install agent-recipes
```

Or install from source:

```bash
git clone https://github.com/MervinPraison/Agent-Recipes.git
cd Agent-Recipes
pip install -e .
```

## Available Templates

| Template | Description | Example | Docs |
|----------|-------------|---------|------|
| `transcript-generator` | Generate transcripts from audio/video files | [examples/](agent_recipes/templates/transcript-generator/examples/) | - |
| `shorts-generator` | Create short-form video clips for social media | [examples/](agent_recipes/templates/shorts-generator/examples/) | - |
| `ai-video-editor` | AI-powered video editing with filler/silence removal | [examples/](agent_recipes/templates/ai-video-editor/examples/) | [README](agent_recipes/templates/ai-video-editor/README.md) |
| `data-transformer` | Transform data between formats with AI mapping | [examples/](agent_recipes/templates/data-transformer/examples/) | - |

## ai-video-editor

```bash
praisonai templates run ai-video-editor --input video.mp4 --output edited.mp4
```

```bash
praisonai templates run ai-video-editor --input video.mp4 --output edited.mp4 --preset podcast
```

```bash
praisonai templates run ai-video-editor --input video.mp4 --tools ./my_tools.py
```

```bash
praisonai templates run ai-video-editor --input video.mp4 --tools-source praisonai_tools.video
```

## Usage

### CLI

```bash
# List available templates
praisonai templates list

# Run a template
praisonai run transcript-generator ./audio.mp3

# Initialize project from template
praisonai init my-project --template transcript-generator
```

### Python API

```python
from praisonaiagents import Workflow

# Load and run a template
workflow = Workflow.from_template("transcript-generator")
result = workflow.run("./audio.mp3")

# With configuration
workflow = Workflow.from_template(
    "data-transformer",
    config={
        "input": "./data.csv",
        "output": "./output.json"
    }
)
```

### From GitHub

```python
from praisonaiagents import Workflow

# Latest version
workflow = Workflow.from_template("github:MervinPraison/Agent-Recipes/transcript-generator")

# Pinned version
workflow = Workflow.from_template("github:MervinPraison/Agent-Recipes/transcript-generator@v1.0.0")
```

## Creating Custom Templates

Templates follow a standard structure:

```
my-template/
├── TEMPLATE.yaml    # Template manifest
├── workflow.yaml    # Workflow definition
├── agents.yaml      # Agent definitions
└── README.md        # Documentation
```

### TEMPLATE.yaml

```yaml
name: my-template
version: "1.0.0"
description: My custom template
author: your-name

requires:
  tools: [tool1, tool2]
  packages: [package1]
  env: [API_KEY]

workflow: workflow.yaml
agents: agents.yaml

config:
  input:
    type: string
    required: true
```

## Contributing

1. Fork the repository
2. Create your template in `templates/`
3. Add entry to `manifest.yaml`
4. Submit a pull request

## License

Apache-2.0
