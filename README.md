### Ehza's system prompt for Claude and ChatGPT

This repository contains system prompts for AI assistants including Claude and ChatGPT, along with specialized prompts for ideation and brainstorming.

## Files

- `ChatGPT-prompt.txt` - Comprehensive system prompt for ChatGPT
- `claude-prompt.txt` - Detailed system prompt for Claude
- `ideate-brainstorm-claude.txt` - Specialized prompt for Claude focused on asking clarifying questions
- `lexicon.txt` - Vocabulary lexicon with advanced terms

## Usage

Use the included `read_prompts.py` utility to read and analyze the prompt files:

```bash
# List available prompts
python3 read_prompts.py --list

# Read a specific prompt (first 50 lines by default)
python3 read_prompts.py --read chatgpt
python3 read_prompts.py --read claude

# Read full content
python3 read_prompts.py --read claude --full

# Show statistics
python3 read_prompts.py --stats
python3 read_prompts.py --stats claude

# Limit output to specific number of lines
python3 read_prompts.py --read ideate --lines 20
```

For help and more options:
```bash
python3 read_prompts.py --help
```
