# Video Editor

AI-powered video editing with natural language commands.

## Features

- **Natural language editing**: Describe edits in plain English
- **Multiple operations**: Trim, effects, audio, text overlays
- **Preview mode**: Generate low-res preview before final render
- **Quality assurance**: Automatic QC checks

## Requirements

- `OPENAI_API_KEY` environment variable
- Optional: `moviepy`, `ffmpeg-python` for video processing
- `ffmpeg` installed on system

## Usage

### CLI

```bash
# Basic editing
praisonai run video-editor ./raw.mp4 -o ./final.mp4 -i "Trim first 10s, add fade in"

# Speed change
praisonai run video-editor ./video.mp4 -i "Speed up 1.5x, add background music"

# Text overlay
praisonai run video-editor ./clip.mp4 -i "Add text 'Hello World' at center"
```

### Python API

```python
from praisonaiagents import Workflow

workflow = Workflow.from_template(
    "video-editor",
    config={
        "input": "./raw.mp4",
        "output": "./final.mp4",
        "instructions": "Trim first 10 seconds, add fade in and out",
        "preview": True
    }
)
result = workflow.run()
```

## Supported Operations

- **Trim/Cut**: Remove sections, extract clips
- **Speed**: Speed up, slow down, reverse
- **Effects**: Fade, blur, color correction, filters
- **Audio**: Volume, mute, add music, extract audio
- **Text**: Overlays, subtitles, watermarks
- **Transitions**: Cross-fade, wipe, dissolve

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input` | string | required | Input video file path |
| `output` | string | auto | Output video file path |
| `instructions` | string | required | Natural language editing instructions |
| `preview` | boolean | true | Generate preview before final render |

## License

Apache-2.0
