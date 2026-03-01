#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILES=("claude-system-prompt.txt" "chatgpt-system-prompt.txt" "claude-mermaid.txt" "ideate-brainstorm-claude.txt" "lexicon.txt" "personality-builder.md")

usage() {
    cat <<EOF
Usage: $(basename "$0") [file|--all|--list]

Read system prompt files from this repository.

Options:
  --list    List available prompt files
  --all     Display all prompt files
  <file>    Display a specific prompt file

Examples:
  $(basename "$0") --list
  $(basename "$0") claude-system-prompt.txt
  $(basename "$0") --all
EOF
}

list_files() {
    echo "Available prompt files:"
    for f in "${PROMPT_FILES[@]}"; do
        if [ -f "$SCRIPT_DIR/$f" ]; then
            echo "  $f"
        fi
    done
}

read_file() {
    local filepath="$SCRIPT_DIR/$1"
    if [ ! -f "$filepath" ]; then
        echo "Error: file not found: $1" >&2
        return 1
    fi
    echo "=== $1 ==="
    echo
    cat "$filepath"
    echo
}

if [ $# -eq 0 ]; then
    usage
    exit 0
fi

case "$1" in
    --list)
        list_files
        ;;
    --all)
        for f in "${PROMPT_FILES[@]}"; do
            if [ -f "$SCRIPT_DIR/$f" ]; then
                read_file "$f"
            fi
        done
        ;;
    --help|-h)
        usage
        ;;
    *)
        read_file "$1"
        ;;
esac
