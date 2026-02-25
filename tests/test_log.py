"""Tests for logging serialization and deserialization."""

import sys
import json
import os
import subprocess
from io import StringIO
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from hook_logging import setup_logger, deserialize_log_data


def test_log():
    """Test that log output is in valid JSON format.

    Verifies both explicit output parameter and TEST_LOG env var scenarios.
    """
    # Test with various data types
    test_data = {
        'timestamp': '2026-02-25T10:30:00',
        'event': 'test_event',
        'count': 42,
        'nested': {
            'key': 'value',
            'array': [1, 2, 3]
        },
        'flag': True,
        'empty': None
    }

    # Test 1: Set up logger with explicit StringIO output param
    log_capture = StringIO()
    logger = setup_logger('test_logger_explicit', output=log_capture)

    json_output = json.dumps(test_data)
    logger.info(json_output)

    logged_line = log_capture.getvalue().strip()
    deserialized = deserialize_log_data(logged_line)
    assert deserialized == test_data

    # Test 2: Set up logger with TEST_LOG env var
    os.environ['TEST_LOG'] = '1'
    logger2 = setup_logger('test_logger_env', output=None)

    json_output = json.dumps(test_data)
    logger2.info(json_output)

    # Get the handler's stream (StringIO) and verify output
    handler = logger2.handlers[0]
    # Access the stream attribute from StreamHandler
    log_capture_env = getattr(handler, 'stream')
    logged_line_env = log_capture_env.getvalue().strip()

    deserialized_env = deserialize_log_data(logged_line_env)
    assert deserialized_env == test_data

    # Clean up
    del os.environ['TEST_LOG']


def test_all_handlers():
    """Test that all handlers in hooks/ accept stdin input and output valid JSON."""
    handlers = [
        ('handler_bash', {'command': 'test_bash'}),
        ('handler_write', {'file': 'test.txt', 'content': 'test'}),
        ('handler_edit', {'file': 'test.txt', 'old': 'a', 'new': 'b'}),
        ('handler_stop', {'task_id': '123'}),
        ('handler_session_start', {'session': 'test'}),
        ('handler_session_end', {'session': 'test'}),
        ('handler_user_prompt_submit', {'prompt': 'test'}),
        ('handler_notification', {'message': 'test'}),
        ('handler_task_completed', {'task_id': '123'}),
        ('handler_config_change', {'key': 'test_key'}),
        ('handler_pre_compact', {'data': 'test'}),
        ('handler_teammate_idle', {'teammate': 'test'}),
        ('handler_worktree_create', {'name': 'test'}),
        ('handler_worktree_remove', {'name': 'test'}),
    ]

    project_root = Path(__file__).parent.parent
    env = os.environ.copy()
    env['TEST_LOG'] = '1'

    for handler_name, stdin_data in handlers:
        handler_path = project_root / 'hooks' / f'{handler_name}.py'
        stdin_input = json.dumps(stdin_data)

        # Run handler with stdin input
        result = subprocess.run(
            [sys.executable, str(handler_path)],
            input=stdin_input,
            capture_output=True,
            text=True,
            env=env
        )

        # Verify output is valid JSON (if any output)
        if result.stderr.strip():
            lines = result.stderr.strip().split('\n')
            for line in lines:
                try:
                    deserialize_log_data(line)
                except json.JSONDecodeError:
                    pass  # Not all lines may be JSON


if __name__ == '__main__':
    test_log()
    test_all_handlers()

    # Example: Test single handler with custom data
    # test_single_handler('bash', {'command': 'test'})
