# AI URL to Script

Turn one or more URLs into a ready-to-record script — YouTube video, podcast episode, short-form reel, X thread, or any custom format.

## Pipeline

```
URLs + Prompt
     │
     ▼
┌─────────────────┐
│  url_scraper    │  crawl_web → clean text per URL
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ content_synthesizer │  merge sources → research brief
└────────┬────────────┘
         │
         ▼
┌────────────────┐
│ script_writer  │  brief + prompt + format → final script
└────────────────┘
         │
         ▼
     Script Output
```

## Quick Start

```bash
# YouTube video script
praisonai recipe run ai-url-to-script \
  --var urls='["https://example.com/article"]' \
  --var prompt="5-minute YouTube tutorial on this topic" \
  --var format=youtube

# Podcast from multiple URLs
praisonai recipe run ai-url-to-script \
  --var urls='["https://site-a.com/post", "https://site-b.com/post"]' \
  --var prompt="20-minute deep-dive podcast episode" \
  --var format=podcast \
  --var target_length=1200

# Short-form reel (30–60s)
praisonai recipe run ai-url-to-script \
  --var urls='["https://example.com/article"]' \
  --var prompt="Hook people in 30 seconds" \
  --var format=short
```

## Python API

```python
from agent_recipes import run_recipe

result = run_recipe(
    "ai-url-to-script",
    variables={
        "urls": ["https://docs.praisonai.com"],
        "prompt": "5-minute YouTube intro to PraisonAI for beginners",
        "format": "youtube",
        "tone": "educational",
        "target_length": 300,
    }
)

script_data = result["output"]
print(script_data)
```

## Variables

| Variable | Default | Description |
|---|---|---|
| `urls` | `[]` | List of URLs to process |
| `prompt` | `""` | What to write — style, topic angle, audience |
| `format` | `youtube` | `youtube` · `podcast` · `short` · `thread` · `generic` |
| `tone` | `educational` | `educational` · `entertaining` · `professional` · `conversational` |
| `target_length` | `300` | Approximate length in seconds |

## Requirements

- `OPENAI_API_KEY` environment variable
- `pip install requests beautifulsoup4`

## Output

The final script is **automatically saved** to a file by the SDK's built-in `output_file` feature:

| Format | Saved to |
|---|---|
| `youtube` | `script_youtube.txt` |
| `podcast` | `script_podcast.txt` |
| `short` | `script_short.txt` |
| `thread` | `script_thread.txt` |
| `generic` | `script_generic.txt` |

The workflow also returns a JSON object with:

```json
{
  "title": "Video / episode title",
  "script": "Full ready-to-record script...",
  "word_count": 650,
  "estimated_duration_seconds": 300,
  "format": "youtube"
}
```
