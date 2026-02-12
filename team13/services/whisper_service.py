"""Whisper client that talks to whisper container to transcribe audio to text."""
import requests
from django.conf import settings


class WhisperClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.base_url = getattr(settings, 'WHISPER_HOST', 'http://whisper:9000')
        return cls._instance

    def transcribe(self, audio_file) -> dict:
        """Send audio file to whisper container"""
        files = {'audio_file': (audio_file.name, audio_file.read(), audio_file.content_type)}
        response = requests.post(
            f"{self.base_url}/asr",
            params={
                "task": "transcribe",
                "language": "en",
                "output": "json"
            },
            files=files
        )
        response.raise_for_status()
        result = response.json()
        return {
            'text': result.get('text', ''),
            'language': result.get('language', 'en'),
        }

whisper_client = WhisperClient()
