# AI Video Thumbnails

Extract thumbnails from video with AI-selected best frame.

## Usage
```bash
praison run ai-video-thumbnails video.mp4
praison run ai-video-thumbnails video.mp4 --count 10
praison run ai-video-thumbnails video.mp4 --interval 30
```

## Output
- `thumbnails/` - Extracted frames
- `best-frame.jpg` - AI-selected best thumbnail
- `grid.jpg` - Contact sheet
- `frames.json` - Frame metadata
