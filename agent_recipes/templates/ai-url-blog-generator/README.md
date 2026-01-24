# AI URL Blog Generator

Generate comprehensive blog posts from any URL with automatic keyword generation, deep research, and WordPress publishing.

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AI URL BLOG GENERATOR PIPELINE                        │
└─────────────────────────────────────────────────────────────────────────────┘

                                    INPUT
                                      │
                                      ▼
                        ┌─────────────────────────┐
                        │   URL to Article        │
                        │   (e.g., blog post,     │
                        │    documentation)       │
                        └───────────┬─────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1: EXTRACT URL CONTENT                                                │
│  ─────────────────────────────                                              │
│  Agent: url_extractor                                                       │
│  Tool: tavily_extract                                                       │
│                                                                             │
│  • Extracts FULL content from URL (no summarization)                        │
│  • Identifies main topic/product name with version                          │
│  • Extracts key points for keyword generation                               │
│                                                                             │
│  Output: extracted_content {topic, content, url, key_points}                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 2: GENERATE SEARCH KEYWORDS                                           │
│  ────────────────────────────────                                           │
│  Agent: keyword_generator                                                   │
│                                                                             │
│  • Analyzes extracted content                                               │
│  • Generates EXACTLY 3 specific search queries:                             │
│    1. Official documentation (site: filter)                                 │
│    2. Technical specifications                                              │
│    3. Code examples/tutorials                                               │
│                                                                             │
│  Output: keywords_data {topic, keywords[]}                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 3: DEEP RESEARCH                                                      │
│  ─────────────────────                                                      │
│  Agent: deep_researcher                                                     │
│  Tool: tavily_search                                                        │
│                                                                             │
│  • Searches with each generated keyword                                     │
│  • Extracts from raw_content field (full page content)                      │
│  • Gathers: dates, statistics, quotes, code examples                        │
│  • Combines with original extracted content                                 │
│                                                                             │
│  Output: research_data {topic, original_content, research, all_facts[]}     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 4: WRITE ARTICLE                                                      │
│  ─────────────────────                                                      │
│  Agent: content_writer                                                      │
│                                                                             │
│  • Uses ALL gathered information (extracted + researched)                   │
│  • Writes in Gutenberg block format                                         │
│  • Adapts to style: coding | news | interactive | comprehensive             │
│  • Creates SEO-optimized title (6-10 words, product name)                   │
│                                                                             │
│  Output: article {title, content}                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 5: PUBLISH TO WORDPRESS                                               │
│  ────────────────────────────                                               │
│  Agent: publisher                                                           │
│  Tool: create_wp_post                                                       │
│                                                                             │
│  • Validates Gutenberg blocks present                                       │
│  • Checks for duplicates                                                    │
│  • Publishes to WordPress                                                   │
│                                                                             │
│  Output: Post ID                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                              ┌───────────┐
                              │  SUCCESS  │
                              │ Post ID:  │
                              │  XXXXX    │
                              └───────────┘
```

## Usage

### Basic Usage

```bash
praisonai recipe run ai-url-blog-generator --var url="https://example.com/article"
```

### With Style Option

```bash
# Coding style (emphasizes code examples)
praisonai recipe run ai-url-blog-generator \
  --var url="https://example.com/article" \
  --var style="coding"

# News style (emphasizes announcements and quotes)
praisonai recipe run ai-url-blog-generator \
  --var url="https://example.com/article" \
  --var style="news"

# Comprehensive style (combines all styles)
praisonai recipe run ai-url-blog-generator \
  --var url="https://example.com/article" \
  --var style="comprehensive"
```

### With Replay Trace (for debugging)

```bash
# Run with trace saving
praisonai recipe run ai-url-blog-generator \
  --save \
  --var url="https://example.com/article"

# List saved traces
praisonai replay list

# View a specific trace
praisonai replay context <session_id>
```

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `url` | `""` | **Required.** URL to extract content from |
| `style` | `"comprehensive"` | Article style: `coding`, `news`, `interactive`, `comprehensive` |
| `keyword_count` | `3` | Number of search keywords to generate |
| `wp_category` | `"AI"` | WordPress category |
| `wp_author` | `"praison"` | WordPress author |

## Requirements

### Environment Variables

- `OPENAI_API_KEY` - OpenAI API key for LLM
- `TAVILY_API_KEY` - Tavily API key for search/extraction

### Packages

```bash
pip install praisonai praisonai-tools praisonaiwp tavily-python
```

## Agents

| Agent | Role | Tools |
|-------|------|-------|
| `url_extractor` | Extracts full content from URL | `tavily_extract` |
| `keyword_generator` | Generates search keywords from content | - |
| `deep_researcher` | Researches topic using keywords | `tavily_search` |
| `content_writer` | Writes article in Gutenberg format | - |
| `publisher` | Publishes to WordPress | `create_wp_post` |

## Output Format

The recipe produces a WordPress post with:

- **Title**: SEO-optimized, 6-10 words, includes product name/version
- **Content**: Gutenberg block format with:
  - Paragraphs (`<!-- wp:paragraph -->`)
  - Headings (`<!-- wp:heading -->`)
  - Code blocks (`<!-- wp:code -->`)
  - Lists (`<!-- wp:list -->`)
  - Tables (`<!-- wp:table -->`)
  - Quotes (`<!-- wp:quote -->`)

## Troubleshooting

### Content Not Extracted

- Verify the URL is accessible
- Check `TAVILY_API_KEY` is set
- Some sites may block extraction

### Keywords Not Generated

- Ensure extracted content contains enough information
- Check the `key_points` in extracted_content

### Article Too Short

- Increase `keyword_count` for more research
- Use `style="comprehensive"` for longer articles

### Duplicate Detected

- The recipe checks for duplicates before publishing
- Modify the URL or wait for unique content

## Version History

- **v2.0.0** - Added keyword generation and deep research pipeline
- **v1.0.0** - Initial release with basic extraction and publishing
