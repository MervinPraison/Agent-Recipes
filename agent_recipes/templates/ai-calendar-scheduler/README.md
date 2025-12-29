# Calendar Scheduler

Parse and schedule events from text to iCal

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-calendar-scheduler <input>

# With output directory
praison recipes run ai-calendar-scheduler <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-calendar-scheduler <input> --dry-run

# Show recipe info
praison recipes info ai-calendar-scheduler

# Check dependencies
praison recipes doctor ai-calendar-scheduler
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-calendar-scheduler")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai
- icalendar

### Environment Variables
- OPENAI_API_KEY

### External Tools
- None

## Tags

`productivity`, `calendar`, `scheduling`

## License

Apache-2.0
