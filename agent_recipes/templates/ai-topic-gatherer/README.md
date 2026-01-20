# AI Topic Gatherer

A standalone modular recipe for discovering current AI news topics.

## Output

Returns a list of 5-10 AI topics with URLs, focusing on:
- Product launches
- Company announcements
- Research papers
- Apps and features
- AI agents

## Usage

### Standalone
```bash
cd ai-topic-gatherer
praisonai workflow run agents.yaml
```

### As Included Module
```yaml
includes:
  - ai-topic-gatherer
```

## Tools Required

- `tavily_search` - For web search
