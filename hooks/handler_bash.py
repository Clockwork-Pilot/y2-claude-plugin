#!/usr/bin/env python3
"""Handler for Bash tool execution.

Blocks Bash invocations whose leading command is denied by proxy_wrapper.py's
namespace deny rules. The same rule fires at runtime via
/usr/local/bin/proxy_wrapper, but blocking pre-flight saves a wasted
invocation and surfaces the deny reason as a tool error.
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from hook_logging import setup_logger
from hooks import is_bash_command_allowed, send_error

logger = setup_logger(__name__)


def main():
    try:
        input_data = sys.stdin.read()
        hook_input = json.loads(input_data) if input_data else {}

        phase = hook_input.get('hook_event_name', '')
        command = hook_input.get('tool_input', {}).get('command', '')
        cwd = hook_input.get('cwd') or os.getcwd()

        # Check proxy_wrapper namespace deny rules
        allowed, reason = is_bash_command_allowed(command, cwd)
        if not allowed:
            error_msg = f"Bash command blocked by proxy_wrapper: {reason}"
            send_error(error_msg)
            log_message = {
                'timestamp': datetime.now().isoformat(),
                'event': 'Bash',
                'phase': phase,
                'status': 'blocked',
                'reason': reason,
                'command': command,
                'data': hook_input,
            }
            logger.error(json.dumps(log_message))
            sys.exit(2)

        log_message = {
            'timestamp': datetime.now().isoformat(),
            'event': 'Bash',
            'phase': phase,
            'command': command,
            'data': hook_input,
        }
        logger.info(json.dumps(log_message))
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error in Bash handler: {e}")
        sys.exit(0)


if __name__ == '__main__':
    main()
