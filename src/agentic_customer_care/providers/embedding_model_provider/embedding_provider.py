from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from utils.config import get_config

load_dotenv()


class OpenAIEmbeddingProvider:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or "text-embedding-3-small"

    def get_embeddings_model(self):
        return OpenAIEmbeddings(model=self.model_name)
    
class HuggingFaceEmbeddingProvider:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or "sentence-transformers/all-MiniLM-L6-v2"

    def get_embeddings_model(self):
        return HuggingFaceEmbeddings(model_name=self.model_name)

class EmbeddingProviderFactory:
    @staticmethod
    def get_embedding_provider(provider_type: str | None = None, model_name: str | None = None):
        provider_type = provider_type or get_config("EMBEDDING_PROVIDER", "huggingface")
        model_name = model_name or get_config("EMBEDDING_MODEL_NAME") or None
        if provider_type == "openai":
            return OpenAIEmbeddingProvider(model_name)
        elif provider_type == "huggingface":
            return HuggingFaceEmbeddingProvider(model_name)
        else:
            raise ValueError(f"Unsupported provider: {provider_type}. Supported types are 'openai' and 'huggingface'.")