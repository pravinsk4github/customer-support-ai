'''
Two important notes:
1. If you are using Groq for LLM, that does not give embeddings.
    You still need embeddings from somewhere else, such as:
    * OpenAI embeddings
    * Hugging Face embeddings
    * local sentence-transformers
2. To keep this project simple and cheap, I would actually recommend HuggingFace embeddings
'''

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_openai import OpenAIEmbeddings

from app.config import settings
from app.core.exception import ServiceUnavailableError
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class VectorService:
    def __init__(self):
        # self.embedding_model = OpenAIEmbeddings()
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=settings.embedding_model_name
        )
        self.vector_store = Chroma(
            collection_name=settings.chroma_collection_name,
            embedding_function=self.embedding_model,
            persist_directory=settings.chroma_persist_directory
        )

    def add_documents(self, documents: list):
        if documents:
            self.vector_store.add_documents(documents)

    def reset_collection(self):
        try:
            self.vector_store.delete_collection()
        except Exception:
            pass

        self.vector_store = Chroma(
            collection_name=settings.chroma_collection_name,
            embedding_function=self.embedding_model,
            persist_directory=settings.chroma_persist_directory
        )

    def get_retriever(self, k: int | None = None):
        search_k = k or settings.retrieval_k
        return self.vector_store.as_retriever(k={"k": search_k})

    def similarity_search_with_score(self, query: str, k: int | None = None):
        try:
            search_k = k or settings.retrieval_k
            return self.vector_store.similarity_search_with_score(query=query, k=search_k)
        except Exception as exc:
            logger.exception(
                "Vector retrieval failed",
                extra={
                    "query": query
                }
            )
            raise ServiceUnavailableError("Knowledge retrieval is temporarily unavailable") from exc