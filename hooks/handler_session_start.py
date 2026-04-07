#!/usr/bin/env python3
"""Handler for SessionStart event."""

import sys
import json
import os

from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from hook_logging import setup_logger
from config import PROJECT_ROOT

logger = setup_logger(__name__)


def main():
    try:
        # Set PROTECTED_REGISTRY_DIR to ensure knowledge_tool creates .protected_files.txt in PROJECT_ROOT
        os.environ['PROTECTED_REGISTRY_DIR'] = str(PROJECT_ROOT)

        input_data = sys.stdin.read()
        hook_input = json.loads(input_data) if input_data else {}

        log_message = {
            'timestamp': datetime.now().isoformat(),
            'event': 'SessionStart',
            'data': hook_input
        }
        logger.info(json.dumps(log_message))
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error in SessionStart handler: {e}")
        sys.exit(0)


if __name__ == '__main__':
    main()
