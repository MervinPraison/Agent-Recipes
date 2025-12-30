# FCP AutoEdit Recipe

AI-powered video editing automation for Final Cut Pro. Converts natural language editing instructions to FCPXML and automatically imports into FCP via CommandPost.

## Prerequisites

- **macOS** - Required for Final Cut Pro
- **Final Cut Pro** - Apple's professional video editing software
- **CommandPost** - Download from [commandpost.io](https://commandpost.io)
- **OpenAI API Key** - Set `OPENAI_API_KEY` environment variable

## Installation

```bash
pip install praisonai openai
```

## Quick Start

```bash
# Simple concatenation
praisonai fcp autoedit --simple --media /path/to/clip1.mov --media /path/to/clip2.mov

# AI-powered editing
praisonai fcp autoedit --instruction "Create a highlight reel with the best moments" \
  --media /path/to/clip1.mov --media /path/to/clip2.mov

# Dry run (generate without importing)
praisonai fcp autoedit --instruction "Add background music" \
  --media /path/to/video.mov --media /path/to/music.mp3 --dry-run
```

## Using as Agent Recipe

```bash
praisonai run fcp-autoedit "Create a 30-second highlight reel" \
  --media /videos/clip1.mov --media /videos/clip2.mov
```

## Python API

```python
from praisonai.integrations.fcp import (
    generate_edit_intent,
    FCPXMLGenerator,
    Injector,
)

# Generate EditIntent from instruction
intent, warnings = generate_edit_intent(
    instruction="Concatenate all clips with crossfades",
    media_paths=["/path/to/clip1.mov", "/path/to/clip2.mov"],
    project_name="My Project",
    format_preset="1080p25",
)

# Generate FCPXML
generator = FCPXMLGenerator(intent)
fcpxml = generator.generate()

# Inject into Final Cut Pro
injector = Injector()
job_id, path, messages = injector.inject_one_shot(fcpxml)
print(f"Injected: {job_id}")
```

## Health Check

```bash
praisonai fcp doctor
```

## One-Time Setup

```bash
praisonai fcp bootstrap-commandpost
```

## Supported Operations (v1)

- ✅ Create projects with primary storyline
- ✅ Place asset clips in sequence
- ✅ Set audio roles (dialogue, music, effects)
- ✅ Add chapter markers
- ✅ Basic volume adjustments

## Not Yet Implemented

- ⏳ Silence/pause removal
- ⏳ Audio normalization (LUFS)
- ⏳ Zoom/Ken Burns effects
- ⏳ Transitions

## Format Presets

- `1080p25`, `1080p30`, `1080p24`, `1080p50`, `1080p60`
- `4k25`, `4k30`, `4k24`, `4k50`, `4k60`
- `720p25`, `720p30`

## Architecture

```
Instruction → EditIntent JSON → FCPXML → CommandPost Watch Folder → FCP Auto-Import
```

The pipeline uses CommandPost's FCPXML watch folder feature for zero-click import into Final Cut Pro.
