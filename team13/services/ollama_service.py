"""Ollama client that talks to separate container - NO LOCAL OLLAMA"""
import requests
from django.conf import settings

class OllamaClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.base_url = getattr(settings, 'OLLAMA_HOST', 'http://ollama:11434')
        return cls._instance

    def grade(self, prompt: str) -> str:
        """Send prompt to Ollama container"""
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": getattr(settings, 'OLLAMA_MODEL', 'gemma3:4b'),
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": 0.1}
            }
        )
        response.raise_for_status()
        return response.json()['message']['content']

ollama_client = OllamaClient()
