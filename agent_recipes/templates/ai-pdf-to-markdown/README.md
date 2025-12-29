# AI PDF to Markdown

Convert PDF documents to clean Markdown format with extracted images.

## Input/Output
- **Input**: PDF file
- **Output**: `document.md`, `images/`, `metadata.json`, `run.json`

## Requirements
- poppler-utils (pdftotext, pdfimages)
- OpenAI API Key (for AI cleanup)

## Usage
```bash
praison run ai-pdf-to-markdown document.pdf
praison run ai-pdf-to-markdown document.pdf --output ./docs/
praison run ai-pdf-to-markdown document.pdf --ocr  # For scanned PDFs
praison run ai-pdf-to-markdown document.pdf --no-images
```
