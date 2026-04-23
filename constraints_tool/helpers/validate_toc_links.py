#!/usr/bin/env python3
"""Validate that all TOC links have matching heading anchors.

This script checks that each link in the table of contents has a corresponding
heading in the document with a matching anchor.

Anchors are generated from heading text using markdown's native anchor generation:
- Lowercase
- Replace spaces and underscores with hyphens
- Remove special characters
- Remove consecutive hyphens

Usage:
    python3 validate_toc_links.py [markdown_file]

Default: task.md
"""

import re
import sys
from pathlib import Path


def generate_anchor(text: str) -> str:
    """Generate markdown anchor from heading text.

    Args:
        text: Heading text to generate anchor for

    Returns:
        Markdown anchor string (without # prefix)
    """
    # Lowercase
    anchor = text.lower()
    # Replace spaces with hyphens (underscores are preserved by markdown renderers)
    anchor = anchor.replace(' ', '-')
    # Remove special characters (keep alphanumeric, hyphens, and underscores)
    anchor = re.sub(r'[^\w-]', '', anchor)
    # Remove consecutive hyphens
    anchor = re.sub(r'-+', '-', anchor)
    # Strip leading/trailing hyphens
    anchor = anchor.strip('-')
    return anchor


def validate_toc_links(markdown_file: str = 'task.md') -> bool:
    """Validate all TOC links have matching anchors.

    Args:
        markdown_file: Path to markdown file to validate

    Returns:
        True if all links are valid, False otherwise
    """
    md_path = Path(markdown_file)
    if not md_path.exists():
        print(f'✗ File not found: {markdown_file}')
        return False

    with open(md_path, 'r') as f:
        content = f.read()

    # Extract TOC links only from the Table of Contents section
    toc_match = re.search(r'## Table of Contents\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not toc_match:
        print('✗ No Table of Contents section found')
        return False

    toc_section = toc_match.group(1)
    # Extract links only from TOC section
    links = re.findall(r'\[([^\]]+)\]\(#([^)]+)\)', toc_section)

    # Extract all headings
    headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)

    # Build set of valid anchors from headings
    anchor_set = {generate_anchor(h) for h in headings}

    # Check each link
    missing = []
    for link_text, anchor in links:
        if anchor not in anchor_set:
            missing.append((link_text, anchor))

    if missing:
        print(f'✗ Found {len(missing)} invalid TOC links:')
        for text, anchor in missing[:5]:
            print(f'  [{text}](#{anchor})')
        if len(missing) > 5:
            print(f'  ... and {len(missing) - 5} more')
        return False
    else:
        print(f'✓ All {len(links)} TOC links have matching anchors')
        return True


if __name__ == '__main__':
    md_file = sys.argv[1] if len(sys.argv) > 1 else 'task.md'
    success = validate_toc_links(md_file)
    sys.exit(0 if success else 1)
