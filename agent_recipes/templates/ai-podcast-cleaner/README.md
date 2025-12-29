# AI Podcast Cleaner

Clean podcast audio by removing noise, normalizing volume, trimming silences, and generating transcripts with chapter markers.

## Input/Output

- **Input**: Audio file (wav, mp3, m4a, flac)
- **Output**:
  - `cleaned.mp3` - Cleaned and normalized audio
  - `transcript.txt` - Plain text transcript
  - `transcript.srt` - SRT caption file
  - `chapters.json` - Chapter markers with timestamps
  - `run.json` - Execution metadata

## Requirements

- **ffmpeg**: Audio processing
- **OpenAI API Key**: For transcription (Whisper)

```bash
# macOS
brew install ffmpeg

# Linux
apt install ffmpeg

# Set API key
export OPENAI_API_KEY=your_key_here
```

## Usage

### CLI

```bash
# Basic usage
praison run ai-podcast-cleaner recording.wav

# With output directory
praison run ai-podcast-cleaner recording.mp3 --output ./cleaned/

# Aggressive cleanup preset
praison run ai-podcast-cleaner recording.wav --preset aggressive

# Skip transcription
praison run ai-podcast-cleaner recording.wav --no-transcribe

# Dry run (show plan without executing)
praison run ai-podcast-cleaner recording.wav --dry-run

# Force overwrite existing output
praison run ai-podcast-cleaner recording.wav --force
```

### Python API

```python
from praisonaiagents import Workflow

workflow = Workflow.from_template("ai-podcast-cleaner")
result = workflow.run(
    input="./recording.wav",
    output="./cleaned/",
    preset="default"
)
```

## Presets

| Preset | Description |
|--------|-------------|
| `default` | Balanced cleanup for most podcasts |
| `aggressive` | Heavy noise reduction, shorter silence threshold |
| `gentle` | Light cleanup, preserves natural pauses |

## Output Files

### cleaned.mp3
- Normalized to -16 LUFS
- Silences > 0.5s removed
- High-quality MP3 (192kbps)

### transcript.txt
Plain text transcript of the audio content.

### transcript.srt
SRT format captions with timestamps:
```
1
00:00:00,000 --> 00:00:05,000
Welcome to the podcast.

2
00:00:05,500 --> 00:00:10,000
Today we're discussing AI agents.
```

### chapters.json
```json
{
  "chapters": [
    {"start": 0, "end": 120, "title": "Introduction"},
    {"start": 120, "end": 480, "title": "Main Discussion"},
    {"start": 480, "end": 600, "title": "Conclusion"}
  ]
}
```

### run.json
Execution metadata including timing, config, and output file info.

## Safety Defaults

- Never modifies input files
- Output to timestamped directory by default
- Requires `--force` to overwrite existing output
- Logs all operations to `run.log`
