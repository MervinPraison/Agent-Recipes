# AI Audio Normalizer

Normalize audio loudness using EBU R128 standard.

## Usage
```bash
praison run ai-audio-normalizer audio.mp3
praison run ai-audio-normalizer audio.wav --target-lufs -14
```

## Output
- `normalized.mp3` - Normalized audio
- `loudness-report.json` - Loudness analysis
