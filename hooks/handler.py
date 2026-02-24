#!/usr/bin/env python3
"""
Unified hook handler for Claude plugin.
Logs all hook invocations with their input arguments.
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import HOOKS_LOG_FILE, HOOKS_LOG_LEVEL

# Configure logging
logging.basicConfig(
    filename=str(HOOKS_LOG_FILE),
    level=getattr(logging, HOOKS_LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main handler function that reads hook input from stdin and logs it.
    Always returns exit code 0 to allow Claude Code to proceed.
    """
    try:
        # Read input from stdin
        input_data = sys.stdin.read()

        # Parse JSON input
        hook_input = json.loads(input_data) if input_data else {}

        # Extract event information
        event = hook_input.get('event', 'Unknown')
        tool_name = hook_input.get('tool', 'Unknown')
        args = hook_input.get('args', {})

        # Log the hook invocation
        log_message = {
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'tool': tool_name,
            'args_keys': list(args.keys()) if isinstance(args, dict) else type(args).__name__
        }

        logger.info(json.dumps(log_message))

        # Return success
        sys.exit(0)

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON input: {e}")
        sys.exit(0)  # Still return 0 to not block Claude Code
    except Exception as e:
        logger.error(f"Error in hook handler: {e}")
        sys.exit(0)  # Still return 0 to not block Claude Code


if __name__ == '__main__':
    main()
