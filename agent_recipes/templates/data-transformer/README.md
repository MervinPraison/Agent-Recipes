# Data Transformer

Transform data between formats with AI-assisted schema mapping.

## Features

- **Multi-format support**: CSV, JSON, XML, Excel
- **AI schema inference**: Automatic detection of data types and patterns
- **Smart mapping**: AI-assisted field mapping between schemas
- **Validation**: Optional output validation

## Requirements

- `OPENAI_API_KEY` environment variable
- Optional: `pandas` for data processing

## Usage

### CLI

```bash
# Basic transformation
praisonai run data-transformer ./data.csv -o ./output.json

# With target schema
praisonai run data-transformer ./legacy.xml -o ./modern.json --schema ./schema.json

# Natural language schema
praisonai run data-transformer ./data.csv -o ./output.json --schema "Salesforce Contact format"
```

### Python API

```python
from praisonaiagents import Workflow

workflow = Workflow.from_template(
    "data-transformer",
    config={
        "input": "./data.csv",
        "output": "./output.json",
        "target_schema": "Salesforce Contact format",
        "validation": True
    }
)
result = workflow.run()
```

## Supported Formats

### Input
- CSV (comma, tab, pipe delimited)
- JSON (objects, arrays)
- XML
- Excel (.xlsx, .xls)

### Output
- JSON
- CSV
- XML
- Excel

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input` | string | required | Input file path |
| `output` | string | required | Output file path |
| `target_schema` | string | auto | Target schema file or description |
| `validation` | boolean | true | Validate output against schema |
| `sample_size` | integer | 100 | Rows to sample for inference |

## License

Apache-2.0
