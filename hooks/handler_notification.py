#!/usr/bin/env python3
"""Handler for Notification event."""

import sys
import os
import json

from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from hook_logging import setup_logger

logger = setup_logger(__name__)


def is_running_in_docker():
    """Check if running inside a Docker container."""
    # Check for .dockerenv file or DOCKER_CONTAINER env var
    return os.path.exists('/.dockerenv') or os.getenv('DOCKER_CONTAINER') == 'true'


def main():
    try:
        input_data = sys.stdin.read()
        hook_input = json.loads(input_data) if input_data else {}

        log_message = {
            'timestamp': datetime.now().isoformat(),
            'event': 'Notification',
            'source': 'input',
            'data': hook_input
        }
        logger.info(json.dumps(log_message))

        # If running in Docker and notification is a permission request, auto-approve
        if is_running_in_docker():
            message = hook_input.get('message', '') if isinstance(hook_input, dict) else ''
            if message.startswith('Claude needs your permission to use'):
                # Auto-respond with Yes
                response_message = 'Yes'
                response_log = {
                    'timestamp': datetime.now().isoformat(),
                    'event': 'NotificationResponse',
                    'source': 'output',
                    'auto_prompt': True,
                    'environment': 'docker',
                    'response_message': response_message,
                    'input_message': message,
                    'decision_reason': 'Auto-approved permission request in Docker environment'
                }
                logger.info(json.dumps(response_log))
                print(response_message)
                sys.exit(0)

        sys.exit(0)
    except Exception as e:
        logger.error(f"Error in Notification handler: {e}")
        sys.exit(0)


if __name__ == '__main__':
    main()
