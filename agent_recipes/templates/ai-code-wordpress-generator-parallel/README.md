# AI Code WordPress Post Generator (Parallel)

Research **AI coding tools, programming methods, and code techniques** for AI Engineers and publish multiple Gutenberg-formatted posts to WordPress **in parallel**.

## Focus Areas

This recipe generates content specifically for **AI Engineers** covering:
- **AI Tools**: Latest AI development tools, SDKs, frameworks, and libraries
- **AI Programming Ideas**: New coding patterns, architectures, and methodologies
- **AI Programming Methods**: Implementation techniques, best practices, algorithms
- **Code Examples**: Practical code snippets, tutorials, and implementations
- **AI Engineering**: Development workflows, toolchains, and productivity

**All articles focus on CODE** - practical, hands-on content for developers building AI systems.

## Features

- **Code-Focused Content**: All articles emphasize code examples and implementations
- **Parallel Processing**: Research and write multiple topics simultaneously
- **Duplicate Detection**: Checks WordPress for existing similar content
- **Batch Duplicate Checking**: Efficiently checks multiple topics at once
- **Gutenberg Format**: Outputs proper WordPress block format with code blocks
- **Modular Design**: Uses include steps for topic gathering

## Requirements

### Environment Variables
- `OPENAI_API_KEY` - OpenAI API key
- `TAVILY_API_KEY` - Tavily search API key

### Packages
```bash
pip install praisonai praisonai-tools praisonaiwp tavily-python
```

### WordPress Configuration
Configure `~/.praisonaiwp/config.yaml` with your WordPress server details.

## Usage

### As a Recipe
```bash
praisonai recipe run ai-code-wordpress-generator-parallel
```

### As a Workflow
```bash
cd /path/to/ai-code-wordpress-generator-parallel
praisonai agents.yaml
```

## How It Works

1. **Gather Topics**: Uses `ai-topic-gatherer` include (configured for AI coding topics)
2. **Filter Duplicates**: Checks each topic against existing WordPress posts
3. **Parallel Research**: Researches multiple topics simultaneously (4 at a time)
4. **Parallel Writing**: Writes code-focused blog posts for each topic in parallel
5. **Publish**: Creates WordPress posts with proper Gutenberg formatting (with code blocks)

## Key YAML Features Used

- `output_variable`: Stores agent output in a named variable
- `loop: over:`: Iterates over a list (auto-parses JSON arrays)
- `parallel: true`: Runs iterations concurrently
- `max_workers`: Limits concurrent executions

## Tools

- `tavily_search` - Search for AI coding tools and techniques
- `crawl_url` - Extract content from URLs
- `check_duplicate` - Check single topic for duplicates
- `check_duplicates_batch` - Check multiple topics at once
- `create_wp_post` - Create WordPress post
