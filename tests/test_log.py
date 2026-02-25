"""Tests for logging serialization and deserialization."""

import sys
import json
from io import StringIO
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from hook_logging import setup_logger, deserialize_log_data


def test_log():
    """Test that logged JSON output is valid and matches original data."""
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

    # Create a StringIO to capture output
    log_capture = StringIO()

    # Set up logger with StringIO output
    logger = setup_logger('test_logger', output=log_capture)

    # Log data as JSON
    json_output = json.dumps(test_data)
    logger.info(json_output)

    # Get the captured output
    logged_line = log_capture.getvalue().strip()

    # Verify it's valid JSON
    assert logged_line, "Log output should not be empty"
    deserialized = deserialize_log_data(logged_line)

    # Verify it matches original data
    assert deserialized == test_data, "Deserialized data should match original"


if __name__ == '__main__':
    test_log()
