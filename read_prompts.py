#!/usr/bin/env python3
"""
System Prompt Reader Utility

A simple command-line utility to read and display system prompts for AI assistants.
"""

import os
import sys
import argparse
from pathlib import Path


class PromptReader:
    """Class to handle reading and displaying prompt files."""
    
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.prompt_files = {
            'chatgpt': 'ChatGPT-prompt.txt',
            'claude': 'claude-prompt.txt', 
            'ideate': 'ideate-brainstorm-claude.txt',
            'lexicon': 'lexicon.txt'
        }
    
    def list_prompts(self):
        """List available prompt files."""
        print("Available prompts:")
        for key, filename in self.prompt_files.items():
            file_path = self.base_path / filename
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"  {key:10} - {filename} ({size} bytes)")
            else:
                print(f"  {key:10} - {filename} (not found)")
    
    def read_prompt(self, prompt_name):
        """Read and return the content of a specific prompt file."""
        if prompt_name not in self.prompt_files:
            raise ValueError(f"Unknown prompt: {prompt_name}")
        
        file_path = self.base_path / self.prompt_files[prompt_name]
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Error reading {file_path}: {e}")
    
    def display_prompt(self, prompt_name, max_lines=None):
        """Display a prompt with optional line limiting."""
        content = self.read_prompt(prompt_name)
        lines = content.splitlines()
        
        print(f"\n=== {self.prompt_files[prompt_name]} ===")
        print(f"Lines: {len(lines)}, Characters: {len(content)}")
        print("=" * 50)
        
        if max_lines and len(lines) > max_lines:
            for i, line in enumerate(lines[:max_lines], 1):
                print(f"{i:3}: {line}")
            print(f"\n... (showing first {max_lines} of {len(lines)} lines)")
            print(f"Use --full to see complete content")
        else:
            for i, line in enumerate(lines, 1):
                print(f"{i:3}: {line}")
    
    def get_stats(self, prompt_name):
        """Get statistics for a prompt file."""
        content = self.read_prompt(prompt_name)
        lines = content.splitlines()
        words = content.split()
        
        return {
            'filename': self.prompt_files[prompt_name],
            'lines': len(lines),
            'characters': len(content),
            'words': len(words),
            'non_empty_lines': len([line for line in lines if line.strip()])
        }
    
    def display_stats(self, prompt_name=None):
        """Display statistics for prompt file(s)."""
        if prompt_name:
            stats = self.get_stats(prompt_name)
            print(f"\nStatistics for {stats['filename']}:")
            print(f"  Lines: {stats['lines']}")
            print(f"  Non-empty lines: {stats['non_empty_lines']}")
            print(f"  Words: {stats['words']}")
            print(f"  Characters: {stats['characters']}")
        else:
            print("\nStatistics for all prompt files:")
            total_stats = {'lines': 0, 'words': 0, 'characters': 0, 'non_empty_lines': 0}
            
            for prompt_name in self.prompt_files.keys():
                try:
                    stats = self.get_stats(prompt_name)
                    print(f"\n{stats['filename']}:")
                    print(f"  Lines: {stats['lines']}")
                    print(f"  Non-empty lines: {stats['non_empty_lines']}")
                    print(f"  Words: {stats['words']}")
                    print(f"  Characters: {stats['characters']}")
                    
                    for key in total_stats:
                        total_stats[key] += stats[key]
                except (FileNotFoundError, ValueError):
                    print(f"\n{self.prompt_files[prompt_name]}: (not found)")
            
            print(f"\nTotal across all files:")
            print(f"  Lines: {total_stats['lines']}")
            print(f"  Non-empty lines: {total_stats['non_empty_lines']}")
            print(f"  Words: {total_stats['words']}")
            print(f"  Characters: {total_stats['characters']}")


def main():
    """Main entry point for the prompt reader utility."""
    parser = argparse.ArgumentParser(
        description="Read and display system prompts for AI assistants",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list                    # List available prompts
  %(prog)s --read chatgpt           # Read ChatGPT prompt
  %(prog)s --read claude --full     # Read full Claude prompt
  %(prog)s --stats                  # Show statistics for all prompts
  %(prog)s --stats claude           # Show statistics for Claude prompt
        """
    )
    
    parser.add_argument('--list', action='store_true',
                       help='List available prompt files')
    parser.add_argument('--read', metavar='PROMPT',
                       help='Read a specific prompt (chatgpt, claude, ideate, lexicon)')
    parser.add_argument('--stats', nargs='?', const='all', metavar='PROMPT',
                       help='Show statistics for prompt(s)')
    parser.add_argument('--full', action='store_true',
                       help='Display full content (default shows first 50 lines)')
    parser.add_argument('--lines', type=int, metavar='N',
                       help='Limit display to N lines')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    try:
        reader = PromptReader()
        
        if args.list:
            reader.list_prompts()
        
        elif args.read:
            max_lines = None if args.full else (args.lines or 50)
            reader.display_prompt(args.read, max_lines)
        
        elif args.stats:
            if args.stats == 'all':
                reader.display_stats()
            else:
                reader.display_stats(args.stats)
        
    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()