#!/usr/bin/env python3
"""Handler for Write tool execution."""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import HOOKS_LOG_FILE, HOOKS_LOG_LEVEL

logging.basicConfig(
    filename=str(HOOKS_LOG_FILE),
    level=getattr(logging, HOOKS_LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    try:
        input_data = sys.stdin.read()
        hook_input = json.loads(input_data) if input_data else {}

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
