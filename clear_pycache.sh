#!/usr/bin/env bash
# A simple utility script to delete Python byte-code caches in the current directory tree.
#
# Usage: ./clear_pycache.sh [path]
# If no path is given, the script will run in the current directory.

set -euo pipefail

# Determine the directory to clean (defaults to current directory)
TARGET_DIR="${1:-.}"

# Ensure the target exists
if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Error: $TARGET_DIR is not a directory." >&2
  exit 1
fi

# Remove __pycache__ directories
find "$TARGET_DIR" -type d -name "__pycache__" -prune -exec rm -rf {} +

# Remove stray *.pyc and *.pyo files (in case they are outside __pycache__)
find "$TARGET_DIR" -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete

echo "Cleared Python byte-code caches in $TARGET_DIR" 