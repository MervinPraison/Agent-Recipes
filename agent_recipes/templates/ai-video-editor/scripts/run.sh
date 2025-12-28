#!/bin/bash
# AI Video Editor - Shell wrapper
# Usage: ./run.sh edit input.mp4 --preset podcast --output out.mp4

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RECIPE_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$RECIPE_DIR/src"

# Run the CLI
cd "$SRC_DIR" && python -m ai_video_editor.cli "$@"
