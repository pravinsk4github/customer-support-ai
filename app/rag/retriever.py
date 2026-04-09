from app.services.vector_service import VectorService

class FAQRetriever:
    def __init__(self, k: int = 4):
        self.vector_service = VectorService()
        self.k = k

    def get_relevant_documents(self, query: str):
        retriever = self.vector_service.get_retriever(k=self.k)
        return self.retriever.invoke(query)

    def get_relevant_documents_with_score(self, query: str):
        return self.vector_service.similarity_search_with_score(query=query, k=self.k)