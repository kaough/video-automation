import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import process_file

class TestWorkflow(unittest.TestCase):
    def test_process_file_success(self):
        # Mock services
        drive_service = MagicMock()
        ai_service = MagicMock()
        youtube_service = MagicMock()
        sheets_service = MagicMock()

        # Setup return values
        drive_service.download_file.return_value = "test_video.mp4"
        ai_service.analyze_video.return_value = {
            "title": "Test Video",
            "description": "A test video description.",
            "thumbnail_prompt": "A test prompt"
        }
        youtube_service.upload_video.return_value = "VIDEO_ID_123"

        # Test data
        file_data = {'id': '123', 'name': 'test_video.mp4'}

        # Run function
        # We mock os.remove to avoid errors
        with patch('os.remove'):
            process_file(file_data, drive_service, ai_service, youtube_service, sheets_service)

        # Assertions
        drive_service.download_file.assert_called_once()
        ai_service.analyze_video.assert_called_once()
        ai_service.generate_thumbnail.assert_called_once()
        youtube_service.upload_video.assert_called_once()
        sheets_service.log_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
