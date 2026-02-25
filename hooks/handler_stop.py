#!/usr/bin/env python3
"""Handler for Stop event."""

import sys
import json

from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from hook_logging import setup_logger

logger = setup_logger(__name__)


def main():
    try:
        input_data = sys.stdin.read()
        hook_input = json.loads(input_data) if input_data else {}

        log_message = {
            'timestamp': datetime.now().isoformat(),
            'event': 'Stop',
            'data': hook_input
        }
        logger.info(json.dumps(log_message))
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error in Stop handler: {e}")
        sys.exit(0)


if __name__ == '__main__':
    main()
