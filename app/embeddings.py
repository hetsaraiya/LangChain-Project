import requests
import numpy as np
from langchain.embeddings.base import Embeddings

from utils.constants import AI_API_ENDPOINT
from utils.exceptions import AIHostUnavailable, APILimitExceeded

class AIEmbeddings(Embeddings):
    def __init__(self, api_key: str, model: str = "text-embedding-3-large"):
        self.api_key = api_key
        self.model = model
        self.endpoint = AI_API_ENDPOINT
        print(self.api_key, "======================================")

    def _get_embedding(self, text: str):
        payload = {
            "input": text,
            "model": self.model
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.post(self.endpoint, json=payload, headers=headers)

        if response.status_code == 429:
            raise APILimitExceeded(f"Error from AI API: {response.text}")
        if response.status_code != 201:
            raise AIHostUnavailable(f"Error from AI API: {response.text}")

        response_data = response.json()
        embedding = response_data["data"][0]["embedding"]
        return np.array(embedding)

    def embed_documents(self, texts):
        """Embeds a list of documents."""
        embeddings = [self._get_embedding(text) for text in texts]
        return embeddings

    def embed_query(self, text):
        """Embeds a single query."""
        return self._get_embedding(text)