# AI Video Editor Recipe

End-to-end AI-powered video editing that automatically cleans up your videos by removing filler words, repetitions, tangents, and long silences.

**This is a self-contained recipe** - no modifications to praisonai or praisonaiagents required.

## Features

- **Automatic Transcription**: Word-level timestamps using OpenAI Whisper
- **Filler Word Removal**: Removes "um", "uh", "like", "you know", etc.
- **Repetition Detection**: Removes stutters and repeated phrases
- **Tangent Removal**: LLM-based detection of off-topic content
- **Silence Removal**: Removes long pauses above configurable threshold
- **Caption Generation**: SRT files or burned-in captions
- **Edit Decision List**: Professional EDL output for further editing

## Requirements

### System Dependencies

- **FFmpeg**: Required for video processing
  ```bash
  # macOS
  brew install ffmpeg
  
  # Linux (Ubuntu/Debian)
  sudo apt install ffmpeg
  
  # Windows
  # Download from https://ffmpeg.org/download.html
  ```

### Python Dependencies

```bash
pip install openai
```

### Environment Variables

```bash
export OPENAI_API_KEY="your-key-here"
```

## Quick Start

### Using Recipe CLI (Recommended)

```bash
# Navigate to recipe directory
cd /path/to/Agent-Recipes/agent_recipes/templates/ai-video-editor/src

# Check dependencies
python -m ai_video_editor.cli doctor

# Edit a video
python -m ai_video_editor.cli edit input.mp4 --preset podcast --output out.mp4

# Probe video metadata
python -m ai_video_editor.cli probe input.mp4

# Generate transcript only
python -m ai_video_editor.cli transcript input.mp4 --output transcript.srt
```

### Using PraisonAI Templates

```bash
# List available templates
praisonai templates list

# Run the template
praisonai templates run ai-video-editor input.mp4 --output edited.mp4
```

### Using Python API

```python
import sys
sys.path.insert(0, "/path/to/Agent-Recipes/agent_recipes/templates/ai-video-editor/src")

from ai_video_editor import edit, probe, transcript

# Simple edit
result = edit(
    input_path="input.mp4",
    preset="podcast",
    output_path="out.mp4",
    verbose=True
)

print(f"Output: {result.output_path}")
print(f"Saved: {result.time_saved:.1f}s")

# Custom settings
result = edit(
    input_path="meeting.mp4",
    remove_fillers=True,
    remove_repetitions=True,
    remove_tangents=True,
    target_length="30m",
    captions="srt",
    verbose=True
)
```

## Presets

| Preset | Fillers | Repetitions | Tangents | Silence Threshold |
|--------|---------|-------------|----------|-------------------|
| podcast | ✓ | ✓ | ✗ | 700ms |
| meeting | ✓ | ✓ | ✓ | 1000ms |
| course | ✓ | ✓ | ✗ | 500ms |
| clean | ✓ | ✓ | ✓ | 600ms |

## Output Files

After editing, you'll find these files in the working directory:

- `*_edited.mp4` - Final edited video
- `transcript.txt` - Plain text transcript
- `captions.srt` - SRT caption file
- `edit_plan.json` - Detailed edit plan with segments
- `edit_decision_list.edl` - Professional EDL file
- `report.json` - Complete processing report

## CLI Reference

### `edit` Command

```bash
python -m ai_video_editor.cli edit <input> [options]

Options:
  --output, -o PATH       Output video path
  --preset PRESET         Edit preset (podcast, meeting, course, clean)
  --remove-fillers        Remove filler words
  --remove-repetitions    Remove repeated phrases
  --remove-tangents       Remove off-topic content
  --auto-crop MODE        Crop mode (off, center, face)
  --target-length TIME    Target duration (e.g., 6m, 90s)
  --captions MODE         Caption mode (off, srt, burn)
  --provider PROVIDER     Transcription provider (openai, local, auto)
  --no-llm                Use simple pattern matching
  --force                 Overwrite output if exists
  --json-report PATH      Save JSON report
  --verbose, -v           Enable verbose output
```

### `probe` Command

```bash
python -m ai_video_editor.cli probe <input> [--json]
```

### `transcript` Command

```bash
python -m ai_video_editor.cli transcript <input> [options]

Options:
  --output, -o PATH       Output file path
  --format FORMAT         Output format (srt, txt, json)
  --provider PROVIDER     Transcription provider
  --language LANG         Language code (default: en)
```

### `doctor` Command

```bash
python -m ai_video_editor.cli doctor
```

## How It Works

1. **Probe**: Extract video metadata (duration, resolution, fps)
2. **Transcribe**: Generate word-level timestamps using Whisper
3. **Analyze**: LLM identifies segments to remove (or simple pattern matching with --no-llm)
4. **Optimize**: Snap cuts to word boundaries, apply padding
5. **Render**: Concatenate kept segments with FFmpeg
6. **Report**: Generate transcript, captions, and edit report

## Tips

- **Start with podcast preset** for general content
- **Use meeting preset** for recordings with off-topic discussion
- **Set target_length** to automatically prioritize cuts
- **Enable verbose mode** to see progress details
- **Check edit_plan.json** to review what was removed
- **Use --no-llm** for faster processing without API calls (after transcription)

## Troubleshooting

### FFmpeg not found

Install FFmpeg for your platform:
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg
```

### API key error

Set your OpenAI API key:
```bash
export OPENAI_API_KEY="sk-..."
```

### Long videos timing out

For videos over 25MB audio, the system automatically chunks the transcription.
For very long videos (>2 hours), consider splitting first.

### Check all dependencies

```bash
python -m ai_video_editor.cli doctor
```

## Architecture

```
ai-video-editor/
├── TEMPLATE.yaml          # Template metadata for discovery
├── README.md              # This file
├── agents.yaml            # Agent definitions
├── workflow.yaml          # Workflow definition
├── requirements.txt       # Python dependencies
├── src/
│   └── ai_video_editor/   # Self-contained Python package
│       ├── __init__.py
│       ├── __main__.py    # Entry point for python -m
│       ├── cli.py         # CLI implementation
│       ├── pipeline.py    # Main orchestrator
│       ├── config.py      # Presets and configuration
│       ├── models.py      # Data models
│       ├── utils.py       # Utilities
│       ├── ffmpeg_probe.py
│       ├── transcribe.py
│       ├── heuristics.py
│       ├── llm_plan.py
│       ├── timeline.py
│       └── render.py
├── tests/                 # Unit tests
├── examples/              # Example configurations
└── scripts/               # Helper scripts
```

## License

Apache-2.0
