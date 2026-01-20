# WordPress Publisher

Modular recipe for publishing content to WordPress.

## Input Format

The recipe expects input with these markers:

```
ARTICLE_TITLE: Your Article Title Here
ARTICLE_CONTENT:
<!-- wp:paragraph -->
<p>Your content in Gutenberg blocks...</p>
<!-- /wp:paragraph -->
```

## Usage

### Standalone

```bash
cd /path/to/templates/wordpress-publisher
praisonai workflow run agents.yaml --input "ARTICLE_TITLE: ..."
```

### From Another Recipe

This recipe is designed to be included from other recipes:

```yaml
# In your recipe's agents.yaml
roles:
  content_writer:
    # ... your content stages ...

# Future: include pattern
include:
  recipe: wordpress-publisher
  input: "{{previous_output}}"
```

## Requirements

- praisonai
- praisonaiwp (configured with SSH access)
- OPENAI_API_KEY

## Features

- Title validation (blocks placeholders, too short titles)
- Session-level deduplication
- Gutenberg block passthrough
- Category and author assignment

## License

Apache-2.0
