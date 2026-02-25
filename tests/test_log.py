"""Tests for logging serialization and deserialization."""

import sys
import json
import os
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


if __name__ == '__main__':
    test_log()
