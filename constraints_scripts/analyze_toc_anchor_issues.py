#!/usr/bin/env python3
"""Analyze TOC anchor issues - identify overly long anchors and usability problems.

This script identifies TOC links with impractically long anchors and suggests
fixing the heading format to use shorter, more practical anchors.

Usage:
    python3 analyze_toc_anchor_issues.py [markdown_file]

Default: task.md
"""

import re
import sys
from pathlib import Path


def analyze_anchor_issues(markdown_file: str = 'task.md'):
    """Analyze and report TOC anchor usability issues."""
    md_path = Path(markdown_file)
    if not md_path.exists():
        print(f'✗ File not found: {markdown_file}')
        return

    with open(md_path, 'r') as f:
        content = f.read()

    # Extract TOC section
    toc_match = re.search(r'## Table of Contents\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not toc_match:
        print('✗ No Table of Contents section found')
        return

    toc_section = toc_match.group(1)
    links = re.findall(r'\[([^\]]+)\]\(#([^)]+)\)', toc_section)

    print("=" * 80)
    print("TOC ANCHOR USABILITY ANALYSIS")
    print("=" * 80)

    # Analyze anchor lengths
    long_anchors = [(text, anchor) for text, anchor in links if len(anchor) > 60]
    medium_anchors = [(text, anchor) for text, anchor in links if 30 < len(anchor) <= 60]
    short_anchors = [(text, anchor) for text, anchor in links if len(anchor) <= 30]

    print(f"\nAnchor Length Distribution:")
    print(f"  Short   (<= 30 chars):    {len(short_anchors):2d} links")
    print(f"  Medium  (31-60 chars):    {len(medium_anchors):2d} links")
    print(f"  LONG    (> 60 chars):     {len(long_anchors):2d} links ⚠")

    print(f"\n" + "=" * 80)
    print(f"PROBLEMATIC LONG ANCHORS (> 60 chars):\n")

    for i, (text, anchor) in enumerate(long_anchors[:10], 1):
        print(f"{i}. [{text}](#{anchor})")
        print(f"   Length: {len(anchor)} characters")
        print(f"   Problem: Anchor is too long for practical use")
        print()

    if len(long_anchors) > 10:
        print(f"   ... and {len(long_anchors) - 10} more long anchors\n")

    print("=" * 80)
    print("ANALYSIS:")
    print("=" * 80)

    if long_anchors:
        print(f"""
✗ ISSUE FOUND: {len(long_anchors)} TOC links have impractically long anchors

Root Cause:
  - TOC links are generated using FULL heading text (ID + full description)
  - Markdown anchor generation includes all text, creating 60+ char anchors
  - These anchors are not user-friendly or copy-paste friendly

Impact:
  - Links technically work but are not practical
  - Manual anchor references are too long
  - Headings need explicit short anchor targets

SOLUTION: Use HTML anchor tags for explicit short anchors

Add HTML comment anchors to headings like:
  <!-- anchor: constraint-bash-render-method -->
  #### constraint_bash_render_method: Verify ConstraintBash has render() method

Then TOC links can target the short anchor:
  [constraint_bash_render_method](#constraint-bash-render-method)
""")
    else:
        print("\n✓ No overly long anchors found")

    print("=" * 80)


if __name__ == '__main__':
    md_file = sys.argv[1] if len(sys.argv) > 1 else 'task.md'
    analyze_anchor_issues(md_file)
