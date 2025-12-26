# Transcript Generator

Generate transcripts from audio/video files using AI speech recognition.

## Features

- **Multi-source input**: Local files or YouTube URLs
- **Language detection**: Automatic or specify language
- **Multiple output formats**: TXT, SRT, VTT, JSON
- **AI cleanup**: Optional LLM-powered transcript cleanup

## Requirements

- `OPENAI_API_KEY` environment variable
- Optional: `youtube_tool` for YouTube URL support

## Usage

### CLI

```bash
# Basic usage
praisonai run transcript-generator ./audio.mp3

# With format
praisonai run transcript-generator ./video.mp4 --format srt

# YouTube URL
praisonai run transcript-generator "https://youtube.com/watch?v=xxx" --language en

# Skip cleanup
praisonai run transcript-generator ./audio.mp3 --no-cleanup
```

### Python API

```python
from praisonaiagents import Workflow

# Load and run template
workflow = Workflow.from_template(
    "transcript-generator",
    config={
        "input": "./audio.mp3",
        "output_format": "srt",
        "language": "en"
    }
)
result = workflow.run()
print(result["output"])
```

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input` | string | required | Audio/video file path or YouTube URL |
| `output_format` | string | "txt" | Output format: txt, srt, vtt, json |
| `language` | string | "auto" | Language code or 'auto' for detection |
| `cleanup` | boolean | true | Apply LLM cleanup for readability |

## Output Formats

### TXT
Plain text with paragraphs.

### SRT (SubRip)
```
1
00:00:00,000 --> 00:00:05,000
First line of transcript.

2
00:00:05,000 --> 00:00:10,000
Second line of transcript.
```

### VTT (WebVTT)
```
WEBVTT

00:00:00.000 --> 00:00:05.000
First line of transcript.

00:00:05.000 --> 00:00:10.000
Second line of transcript.
```

### JSON
```json
{
  "segments": [
    {"start": 0.0, "end": 5.0, "text": "First line"},
    {"start": 5.0, "end": 10.0, "text": "Second line"}
  ],
  "language": "en",
  "duration": 10.0
}
```

## License

Apache-2.0
