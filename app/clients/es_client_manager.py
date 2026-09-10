import asyncio
import requests
from langchain_core.embeddings import Embeddings
from app.conf.app_config import EmbeddingConfig, app_config


class TEIEmbeddings(Embeddings):
    """调用 Text Embeddings Inference (TEI) 服务"""

    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url.rstrip("/")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        response = requests.post(
            f"{self.endpoint_url}/embed",
            json={"inputs": texts},
            timeout=120,
        )
        response.raise_for_status()
        return response.json()

    def embed_query(self, text: str) -> list[float]:
        response = requests.post(
            f"{self.endpoint_url}/embed",
            json={"inputs": text},
            timeout=120,
        )
        response.raise_for_status()
        return response.json()

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        return await asyncio.to_thread(self.embed_documents, texts)

    async def aembed_query(self, text: str) -> list[float]:
        return await asyncio.to_thread(self.embed_query, text)


class EmbeddingClientManager:
    def __init__(self, config: EmbeddingConfig):
        self.client: TEIEmbeddings | None = None
        self.config = config

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        self.client = TEIEmbeddings(
            endpoint_url=self._get_url()
        )


embedding_client_manager = EmbeddingClientManager(app_config.embedding)


if __name__ == "__main__":
    embedding_client_manager.init()
    client = embedding_client_manager.client

    async def test():
        text = "What is deep learning?"

        query_result = await client.aembed_query(text)

        print("向量维度:", len(query_result))
        print("前3个值:", query_result[:3])

    asyncio.run(test())