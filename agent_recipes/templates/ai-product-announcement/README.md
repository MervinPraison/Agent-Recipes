# AI Product Announcement

A 3-stage marketing post generator for product announcements.

## Stages

1. **product_researcher** - Gathers comprehensive product information
2. **announcement_writer** - Creates engaging marketing content
3. **includes: wordpress-publisher** - Uses the modular publisher recipe

## Usage

```bash
cd ai-product-announcement
praisonai workflow run agents.yaml --input "iPhone 16 Pro"
```

## Modular Architecture

This recipe uses the `includes:` pattern to reuse the `wordpress-publisher` recipe
for the final publishing stage, demonstrating DRY (Don't Repeat Yourself) principles.

## Output Format

The announcement_writer produces:
```
ARTICLE_TITLE: Exciting Product Announcement Headline
ARTICLE_CONTENT: <!-- wp:paragraph -->
<p>Compelling marketing content...</p>
<!-- /wp:paragraph -->
```
