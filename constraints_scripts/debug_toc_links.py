#!/usr/bin/env python3
"""Debug TOC link mappings - show which headings each TOC link points to.

This script extracts TOC links and shows what headings they match to,
helping identify broken or mismatched links.

Usage:
    python3 debug_toc_links.py [markdown_file]

Default: task.k.md
"""

import re
import sys
from pathlib import Path


def generate_anchor(text: str) -> str:
    """Generate markdown anchor matching Task._generate_anchor logic."""
    anchor = text.lower()
    anchor = anchor.replace(' ', '-').replace('_', '-')
    anchor = re.sub(r'[^\w-]', '', anchor)
    anchor = re.sub(r'-+', '-', anchor)
    anchor = anchor.strip('-')
    return anchor


def debug_toc_links(markdown_file: str = 'task.k.md') -> bool:
    """Debug and show TOC link mappings.

    Args:
        markdown_file: Path to markdown file to debug

    Returns:
        True if all links are valid, False otherwise
    """
    md_path = Path(markdown_file)
    if not md_path.exists():
        print(f'✗ File not found: {markdown_file}')
        return False

    with open(md_path, 'r') as f:
        content = f.read()

    # Extract TOC section
    toc_match = re.search(r'## Table of Contents\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not toc_match:
        print('✗ No Table of Contents section found')
        return False

    toc_section = toc_match.group(1)
    links = re.findall(r'\[([^\]]+)\]\(#([^)]+)\)', toc_section)

    # Extract all headings
    headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)

    # Build map of anchors to headings
    anchor_to_heading = {}
    for heading in headings:
        anchor = generate_anchor(heading)
        anchor_to_heading[anchor] = heading

    print(f"TOC Link Mapping Report")
    print("=" * 80)
    print(f"\nFound {len(links)} TOC links")
    print(f"Found {len(headings)} headings\n")

    # Group links by indent level
    indent_0_valid = 0
    indent_1_valid = 0
    indent_2_valid = 0
    invalid = []

    # Get full TOC lines to preserve indentation info
    toc_lines = toc_section.split('\n')
    link_count = 0

    for line in toc_lines:
        # Check if line contains a link
        match = re.search(r'\[([^\]]+)\]\(#([^)]+)\)', line)
        if not match:
            continue

        link_text = match.group(1)
        anchor = match.group(2)

        # Determine indent level
        indent = len(line) - len(line.lstrip())
        indent_level = indent // 2  # Each indent is 2 spaces

        if anchor in anchor_to_heading:
            heading = anchor_to_heading[anchor]
            status = "✓"
            if indent_level == 0:
                indent_0_valid += 1
            elif indent_level == 1:
                indent_1_valid += 1
            elif indent_level == 2:
                indent_2_valid += 1
        else:
            heading = "NOT FOUND"
            status = "✗"
            invalid.append((link_text, anchor, indent_level))

        # Show first few and last few links
        link_count += 1
        if link_count <= 5 or link_count > len(links) - 2:
            indent_str = "  " * indent_level
            print(f"{status} {indent_str}[{link_text}](#{anchor})")
            print(f"  {indent_str}→ {heading[:70]}")

    if len(links) > 10:
        print(f"\n... ({len(links) - 7} more links) ...\n")

    print("\n" + "=" * 80)
    print(f"Summary:")
    print(f"  Level 0 (Features):     {indent_0_valid} valid")
    print(f"  Level 1 (Constraints):  {indent_1_valid} valid")
    print(f"  Level 2 (Details):      {indent_2_valid} valid")

    if invalid:
        print(f"\n✗ {len(invalid)} invalid links found:")
        for text, anchor, level in invalid[:10]:
            indent_str = "  " * level
            print(f"  {indent_str}[{text}](#{anchor})")
        return False
    else:
        print(f"\n✓ All {len(links)} TOC links are valid!")
        return True


if __name__ == '__main__':
    md_file = sys.argv[1] if len(sys.argv) > 1 else 'task.md'
    success = debug_toc_links(md_file)
    sys.exit(0 if success else 1)
