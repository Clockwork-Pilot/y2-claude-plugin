"""
Format validation tests for task management system.

Tests RFC 3339 timestamp format, markdown structure, and document format compliance.
"""
import pytest
from datetime import datetime, timezone
from pathlib import Path
import tempfile
from tasks_scripts.task_create import create_task
from tasks_scripts.task_roll import advance_phase
from tasks_scripts.task_state import load_task_document

class TestRFC3339Format:
    """Test RFC 3339 timestamp format validation."""
    
    def test_timestamps_are_rfc3339_format(self, tmp_path):
        """All timestamps should be RFC 3339 format (ISO 8601)."""
        task_path = tmp_path / ".TASK.md"
        doc = create_task(str(task_path))
        
        # Check created_at is RFC 3339
        timestamp = doc.created_at
        iso_str = timestamp.isoformat()
        
        # RFC 3339 format: YYYY-MM-DDTHH:MM:SS[.ffffff]±HH:MM or Z
        assert "T" in iso_str, "Timestamp missing T separator"
        assert ":" in iso_str, "Timestamp missing timezone info"
        
    def test_phase_headers_contain_rfc3339_timestamp(self, tmp_path):
        """Phase headers should contain RFC 3339 timestamps."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))
        advance_phase(str(task_path))
        
        content = task_path.read_text()
        
        # Check all phase headers have valid timestamps
        import re
        phase_pattern = r"^# PHASE\s+(\S+)\s+at\s+(.+)$"
        matches = re.finditer(phase_pattern, content, re.MULTILINE)
        
        for match in matches:
            timestamp_str = match.group(2)
            # Should be valid RFC 3339
            try:
                datetime.fromisoformat(timestamp_str)
            except ValueError:
                pytest.fail(f"Invalid RFC 3339 timestamp: {timestamp_str}")

class TestMarkdownFormat:
    """Test markdown structure and formatting."""
    
    def test_phase_headers_format(self, tmp_path):
        """Phase headers should follow: # PHASE <name> at <timestamp>"""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))
        content = task_path.read_text()
        
        import re
        pattern = r"^# PHASE\s+\S+\s+at\s+\d{4}-\d{2}-\d{2}T"
        assert re.search(pattern, content, re.MULTILINE), "Invalid phase header format"
    
    def test_section_markers_format(self, tmp_path):
        """Section markers should be HTML comments: <!-- PHASE_NAME -->"""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))
        content = task_path.read_text()
        
        import re
        pattern = r"<!--\s*\w+(?:\.\w+)*\s*-->"
        assert re.search(pattern, content), "Invalid section marker format"
    
    def test_document_structure_consistency(self, tmp_path):
        """Document structure should be consistent across phases."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))
        
        # Advance through multiple phases
        for _ in range(3):
            advance_phase(str(task_path))
        
        doc = load_task_document(str(task_path))
        
        # All phases should have valid headers
        for phase in doc.phases:
            assert phase.header.phase_name, "Phase missing name"
            assert phase.header.timestamp, "Phase missing timestamp"
            assert isinstance(phase.header.timestamp, datetime), "Timestamp not datetime"

class TestContentFormat:
    """Test content formatting rules."""
    
    def test_initial_task_content_not_empty(self, tmp_path):
        """Initial task should have content."""
        task_path = tmp_path / ".TASK.md"
        doc = create_task(str(task_path))
        
        assert doc.phases[0].content.strip(), "Initial phase content is empty"
    
    def test_markers_removed_from_displayed_content(self, tmp_path):
        """Section markers should not appear in Phase.content."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))
        doc = load_task_document(str(task_path))
        
        for phase in doc.phases:
            assert "<!--" not in phase.content, f"Marker found in content: {phase.content}"
            assert "-->" not in phase.content, f"Marker found in content: {phase.content}"
    
    def test_phase_names_follow_naming_convention(self, tmp_path):
        """Phase names should follow SECTION.SUBSECTION format."""
        task_path = tmp_path / ".TASK.md"
        create_task(str(task_path))
        
        doc = load_task_document(str(task_path))
        
        for phase in doc.phases:
            name = phase.header.phase_name
            # Should have at least one dot (TASK_PLAN.DEFINE, EXEC_EVAL.TESTING)
            parts = name.split(".")
            assert len(parts) >= 2, f"Invalid phase name format: {name}"
            # Each part should be uppercase with underscores
            for part in parts:
                assert part.isupper(), f"Phase part not uppercase: {part}"
                assert all(c.isalnum() or c == "_" for c in part), f"Invalid chars in phase: {part}"

class TestTimestampPrecision:
    """Test timestamp precision and consistency."""
    
    def test_timestamps_have_timezone_info(self, tmp_path):
        """All timestamps should include timezone information."""
        task_path = tmp_path / ".TASK.md"
        doc = create_task(str(task_path))
        
        # Check that timestamp has timezone
        assert doc.created_at.tzinfo is not None, "Timestamp missing timezone"
        
        # Check phase timestamps
        for phase in doc.phases:
            assert phase.header.timestamp.tzinfo is not None, "Phase timestamp missing timezone"
    
    def test_timestamps_use_utc(self, tmp_path):
        """Timestamps should use UTC timezone."""
        task_path = tmp_path / ".TASK.md"
        doc = create_task(str(task_path))
        
        # Created timestamp should be UTC
        assert doc.created_at.tzinfo.tzname(doc.created_at) == "UTC", "Not UTC timezone"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
