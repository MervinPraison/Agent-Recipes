# Agent Recipes

Pre-built, distributable AI agent workflows with dependency management.

## Templates vs Project Config

| Concept | What It Is | When to Use |
|---------|------------|-------------|
| **Project Config** (`agents.yaml` + `tools.py`) | Local, ad-hoc agent definition in your working directory | Rapid prototyping, local development, quick iteration |
| **Templates/Recipes** (this repo) | Distributable, versioned agent bundles with dependency checking | Sharing workflows, reproducible pipelines, production use |

**Key Differences:**
- **Project Config**: No dependency management, no versioning, not portable
- **Templates**: Explicit `requires` (packages, env vars, external tools), versioned, discoverable via CLI

## Installation

| Command | Description |
|---------|-------------|
| `pip install agent-recipes` | Install from PyPI |
| `pip install -e .` | Install from source |

## CLI Commands

| Command | Description |
|---------|-------------|
| `praison templates list` | List available recipes |
| `praison templates info <recipe>` | Show recipe details |
| `praison templates run <recipe> <input>` | Run a recipe |
| `praison templates run <recipe> <input> --dry-run` | Preview without executing |
| `praison templates run <recipe> <input> --output <dir>` | Specify output directory |
| `praison templates run <recipe> <input> --force` | Overwrite existing output |

## Video/Audio Recipes

| Recipe | CLI Command | Docs |
|--------|-------------|------|
| `ai-podcast-cleaner` | `praison templates run ai-podcast-cleaner recording.wav` | [README](agent_recipes/templates/ai-podcast-cleaner/README.md) |
| `ai-video-to-gif` | `praison templates run ai-video-to-gif video.mp4` | [README](agent_recipes/templates/ai-video-to-gif/README.md) |
| `ai-audio-splitter` | `praison templates run ai-audio-splitter audio.mp3` | [README](agent_recipes/templates/ai-audio-splitter/README.md) |
| `ai-video-thumbnails` | `praison templates run ai-video-thumbnails video.mp4` | [README](agent_recipes/templates/ai-video-thumbnails/README.md) |
| `ai-audio-normalizer` | `praison templates run ai-audio-normalizer audio.mp3` | [README](agent_recipes/templates/ai-audio-normalizer/README.md) |
| `ai-video-editor` | `praison templates run ai-video-editor video.mp4` | [README](agent_recipes/templates/ai-video-editor/README.md) |
| `transcript-generator` | `praison templates run transcript-generator audio.mp3` | [README](agent_recipes/templates/transcript-generator/README.md) |

## Document Recipes

| Recipe | CLI Command | Docs |
|--------|-------------|------|
| `ai-pdf-to-markdown` | `praison templates run ai-pdf-to-markdown document.pdf` | [README](agent_recipes/templates/ai-pdf-to-markdown/README.md) |
| `ai-markdown-to-pdf` | `praison templates run ai-markdown-to-pdf document.md` | [README](agent_recipes/templates/ai-markdown-to-pdf/README.md) |
| `ai-pdf-summarizer` | `praison templates run ai-pdf-summarizer document.pdf` | [README](agent_recipes/templates/ai-pdf-summarizer/README.md) |
| `ai-slide-to-notes` | `praison templates run ai-slide-to-notes presentation.pdf` | [README](agent_recipes/templates/ai-slide-to-notes/README.md) |
| `ai-doc-translator` | `praison templates run ai-doc-translator document.md --language es` | [README](agent_recipes/templates/ai-doc-translator/README.md) |

## Image Recipes

| Recipe | CLI Command | Docs |
|--------|-------------|------|
| `ai-image-optimizer` | `praison templates run ai-image-optimizer ./images/` | [README](agent_recipes/templates/ai-image-optimizer/README.md) |
| `ai-image-cataloger` | `praison templates run ai-image-cataloger ./photos/` | [README](agent_recipes/templates/ai-image-cataloger/README.md) |
| `ai-screenshot-ocr` | `praison templates run ai-screenshot-ocr screenshot.png` | [README](agent_recipes/templates/ai-screenshot-ocr/README.md) |
| `ai-image-resizer` | `praison templates run ai-image-resizer ./images/` | [README](agent_recipes/templates/ai-image-resizer/README.md) |

## Code/Repo Recipes

| Recipe | CLI Command | Docs |
|--------|-------------|------|
| `ai-repo-readme` | `praison templates run ai-repo-readme ./my-project` | [README](agent_recipes/templates/ai-repo-readme/README.md) |
| `ai-changelog-generator` | `praison templates run ai-changelog-generator ./my-repo` | [README](agent_recipes/templates/ai-changelog-generator/README.md) |
| `ai-code-documenter` | `praison templates run ai-code-documenter ./src/` | [README](agent_recipes/templates/ai-code-documenter/README.md) |
| `ai-dependency-auditor` | `praison templates run ai-dependency-auditor ./my-project` | [README](agent_recipes/templates/ai-dependency-auditor/README.md) |

## Data Recipes

| Recipe | CLI Command | Docs |
|--------|-------------|------|
| `ai-csv-cleaner` | `praison templates run ai-csv-cleaner data.csv` | [README](agent_recipes/templates/ai-csv-cleaner/README.md) |
| `ai-json-to-csv` | `praison templates run ai-json-to-csv data.json` | [README](agent_recipes/templates/ai-json-to-csv/README.md) |
| `ai-data-profiler` | `praison templates run ai-data-profiler data.csv` | [README](agent_recipes/templates/ai-data-profiler/README.md) |
| `ai-schema-generator` | `praison templates run ai-schema-generator data.json` | [README](agent_recipes/templates/ai-schema-generator/README.md) |
| `data-transformer` | `praison templates run data-transformer data.csv` | [README](agent_recipes/templates/data-transformer/README.md) |

## Web Recipes

| Recipe | CLI Command | Docs |
|--------|-------------|------|
| `ai-url-to-markdown` | `praison templates run ai-url-to-markdown https://example.com/article` | [README](agent_recipes/templates/ai-url-to-markdown/README.md) |
| `ai-sitemap-scraper` | `praison templates run ai-sitemap-scraper https://example.com/sitemap.xml` | [README](agent_recipes/templates/ai-sitemap-scraper/README.md) |

## Packaging Recipes

| Recipe | CLI Command | Docs |
|--------|-------------|------|
| `ai-folder-packager` | `praison templates run ai-folder-packager ./my-project` | [README](agent_recipes/templates/ai-folder-packager/README.md) |

## Recipe Options

| Option | Description |
|--------|-------------|
| `--output`, `-o` | Output directory |
| `--dry-run` | Show plan without executing |
| `--force` | Overwrite existing output |
| `--verbose`, `-v` | Enable verbose output |
| `--preset` | Use a preset configuration |
| `--config` | Path to config file |

## License

Apache-2.0
