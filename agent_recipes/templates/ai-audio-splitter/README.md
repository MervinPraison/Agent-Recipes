# AI Audio Splitter

Split long audio files by silence detection or chapter markers.

## Usage
```bash
praison run ai-audio-splitter long_audio.mp3
praison run ai-audio-splitter podcast.wav --min-silence 2.0
```

## Output
- `tracks/` - Split audio tracks
- `manifest.json` - Track metadata
- `run.json` - Execution metadata
