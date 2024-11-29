# tests/test_note_processor.py
import pytest
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_process_note():
    with patch('openai.AsyncOpenAI') as mock_openai:
        mock_openai.return_value.chat.completions.acreate.return_value = \
            MagicMock(choices=[MagicMock(message=MagicMock(content="Test summary"))])
        
        processor = NoteProcessor()
        result = await processor.process_note("Test content")
        
        assert result["processed_content"] == "Test summary"
        assert result["language"] == "en"