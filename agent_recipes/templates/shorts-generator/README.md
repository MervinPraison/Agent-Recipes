# Shorts Generator

Generate short-form video clips from long videos for social media platforms.

## Features

- **Multi-platform support**: TikTok, YouTube Shorts, Instagram Reels
- **AI content analysis**: Identifies viral-worthy moments
- **Auto-captioning**: Platform-optimized captions
- **Multiple aspect ratios**: 9:16, 1:1, 16:9

## Requirements

- `OPENAI_API_KEY` environment variable
- Optional: `moviepy`, `pillow` for video processing

## Usage

### CLI

```bash
# Basic usage
praisonai run shorts-generator ./video.mp4

# Custom settings
praisonai run shorts-generator ./video.mp4 --duration 30 --clips 5

# Different aspect ratio
praisonai run shorts-generator ./video.mp4 --aspect 1:1
```

### Python API

```python
from praisonaiagents import Workflow

workflow = Workflow.from_template(
    "shorts-generator",
    config={
        "input": "./video.mp4",
        "duration": 45,
        "num_clips": 5,
        "caption_style": "bold"
    }
)
result = workflow.run()
```

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input` | string | required | Video file path or YouTube URL |
| `duration` | integer | 60 | Target clip duration (15-90 seconds) |
| `aspect_ratio` | string | "9:16" | Aspect ratio: 9:16, 1:1, 16:9 |
| `caption_style` | string | "modern" | Caption style: modern, classic, minimal, bold |
| `num_clips` | integer | 3 | Number of clips to generate |

## License

Apache-2.0
