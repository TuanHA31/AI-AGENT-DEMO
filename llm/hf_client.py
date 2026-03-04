import requests
import os

class HFChat:
    def __init__(self, api_key, model):
        self.url = "https://router.huggingface.co/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.model = model

    def chat(self, messages):
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }

        response = requests.post(self.url, headers=self.headers, json=payload)
        return response.json()["choices"][0]["message"]["content"]