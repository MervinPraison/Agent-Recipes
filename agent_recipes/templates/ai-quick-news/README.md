# AI Quick News

A simple 2-stage news article generator that demonstrates modular recipe composition.

## Stages

1. **news_writer** - Searches and writes a quick news article
2. **includes: wordpress-publisher** - Uses the modular publisher recipe

## Usage

```bash
cd ai-quick-news
praisonai workflow run agents.yaml
```

Or with a specific topic:

```bash
praisonai workflow run agents.yaml --input "Latest AI chip developments"
```

## Modular Architecture

This recipe demonstrates the `includes:` pattern for modular recipe composition.
Instead of duplicating the WordPress publishing logic, it includes the standalone
`wordpress-publisher` recipe.

## Output Format

The news_writer produces output in this format:
```
ARTICLE_TITLE: Your Title Here
ARTICLE_CONTENT: <!-- wp:paragraph -->
<p>Content here...</p>
<!-- /wp:paragraph -->
```

The included `wordpress-publisher` recipe then extracts and publishes this content.
