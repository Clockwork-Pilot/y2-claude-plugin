#!/usr/bin/env python3
"""Handler for Write tool execution.

Blocks writes to registered knowledge files. If a file is registered in
protected_files.txt, exits with code 2 to prevent direct modification.
Knowledge files should only be updated via patch_knowledge_document.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from hook_logging import setup_logger
from hooks import is_knowledge_file, is_edit_blocked_by_unverified_constraints, send_error, get_deny_reasons_for_file

logger = setup_logger(__name__)


def main():
    try:
        input_data = sys.stdin.read()
        hook_input = json.loads(input_data) if input_data else {}

        # Check if writing is blocked due to unverified constraints
        file_path = hook_input.get('tool_input', {}).get('file_path')
        if is_edit_blocked_by_unverified_constraints(file_path):
            error_msg = "Cannot write: spec.k.json contains unverified constraints.\n\nUnverified constraints must be removed or fixed before modifications are allowed."
            send_error(error_msg, file_path)
            logger.error(f"Write blocked due to unverified constraints: {file_path}")
            sys.exit(2)

        # Check file-rules deny list
        if file_path:
            reasons = get_deny_reasons_for_file(file_path)
            if reasons:
                error_msg = f"Cannot write {file_path}: denied by file rules: {', '.join(reasons)}"
                send_error(error_msg, file_path)
                logger.error(f"Write blocked by file rules {reasons}: {file_path}")
                sys.exit(2)

        # Check if the file being written is a registered knowledge file
        # Hook input has file_path in tool_input (actual structure from hook data)
        if file_path and is_knowledge_file(file_path):
            error_msg = f"Cannot write to knowledge document: {file_path}\n\nKnowledge documents should only be modified using patch_knowledge_document.py to ensure proper validation and automatic markdown rendering."
            send_error(error_msg, file_path)
            logger.error(f"Attempted to write to registered knowledge file: {file_path}")
            sys.exit(2)

        log_message = {
            'timestamp': datetime.now().isoformat(),
            'event': 'Write',
            'data': hook_input
        }
        logger.info(json.dumps(log_message))
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error in Write handler: {e}")
        sys.exit(0)


if __name__ == '__main__':
    main()
