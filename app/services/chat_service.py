from langchain_core.documents import Document
from sqlalchemy.orm import Session

from app.config import settings
from app.core.exception import NotFoundError
from app.repositories.chat_repository import ChatRepository
from app.rag.retriever import FAQRetriever
from app.rag.chains import build_support_chain
from app.schemas import ChatMessageCreate
from app.services.llm_service import get_llm
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.chat_repository = ChatRepository(db)
        self.retriever = FAQRetriever(k=4)
        self.llm = get_llm()
        self.chain = build_support_chain(self.llm)

    def _format_history(self, messages: list[ChatMessageCreate]) -> str:
        if not messages:
            return "No previous conversation found."
        return "\n".join(f"{msg.role}: {msg.message}" for msg in messages)

    def _build_retrieval_query(self, history_text: str, user_message: str) -> str:
        return (
            f"Recent conversation:\n{history_text}\n\n"
            f"Current Use question:\n{user_message}"
        )

    def _select_best_document(self, scored_documents):
        if not scored_documents:
            return []

        ranked_results = sorted(scored_documents, key=lambda x: x[1])
        best_doc, best_score = ranked_results[0]

        logger.info(
            "best_retrieval score=%.4f faq_id=%s category=%s",
            best_score,
            best_doc.metadata.get("faq_id"),
            best_doc.metadata.get("category")
        )
        
        # absolute threshold check
        if best_score > settings.retrieval_score_threshold:
            logger.info("fallback_triggered reason=score_threshold best_score=%.4f threshold=%.4f",
                best_score,
                settings.retrieval_score_threshold
            )
            return []

        # relative confidence check (only if we have > 1 results)
        if len(ranked_results) > 1:
            second_doc, second_score = ranked_results[1]
            score_gap = second_score - best_score

            logger.info(
                "second_retrieval score=%.4f faq_id=%s category=%s score_gap=%.4f",
                second_score,
                second_doc.metadata.get("faq_id"),
                second_doc.metadata.get("category"),
                score_gap
            )

            if score_gap < settings.retrieval_min_score_gap:
                logger.info(
                    "fallback_triggered reason=low_score_gap best_score=%.4f second_score=%.4f gap=%.4f min_gap=%.4f",
                    best_score,
                    second_score,
                    score_gap,
                    settings.retrieval_min_score_gap,
                )

        logger.info("accepted_docs_count=1")
        return [best_doc]

    def _format_context(self, documents) -> str:
        if not documents:
            return "No relevant support knowlwdge found."
        
        return "\n\n".join(doc.page_content for doc in documents)

    def _fallback_response(self) -> str:
        return (
            "I’m sorry, but I don’t have enough context to answer that accurately. "
            "Could you please clarify which point you mean or provide a bit more detail?"
        )
 
    def ask(self, session_id: str, user_message: str) -> dict:
        logger.info("chat_request session=%s message=%s", session_id, user_message)
        self.chat_repository.create_session_if_not_exists(session_id)

        recent_messages = self.chat_repository.get_recent_messages(
            session_id=session_id, 
            limit=6
        )

        history_text = self._format_history(recent_messages)
        retrieval_query = self._build_retrieval_query(history_text, user_message)
        scored_docs = self.retriever.get_relevant_documents_with_score(retrieval_query)

        for doc, score in scored_docs:
            print(f"Score: {score}")
            print(f"Content: {doc.page_content}")
            print(f"Metadata: {doc.metadata}")
            print("------------------------------------")

        filtered_docs = self._select_best_document(scored_docs)

        self.chat_repository.add_message(
            ChatMessageCreate(
                session_id=session_id,
                role="user",
                message=user_message
            )
        )

        if not filtered_docs:
            logger.info("fallback_triggered session_id=%s", session_id)

            answer = self._fallback_response()
            self.chat_repository.add_message(
                    ChatMessageCreate(
                    session_id=session_id,
                    role="assistant",
                    message=answer
                )
            )
            return {
                "session_id": session_id,
                "answer": answer,
                "sources": []
            }

        context_text = self._format_context(filtered_docs)
        
        answer = self.chain.invoke(
            {
                "history": history_text,
                "context": context_text,
                "question": user_message
            }
        )
        
        self.chat_repository.add_message(
            ChatMessageCreate(
                session_id=session_id,
                role="assistant",
                message=answer
            )
        )

        sources = [
            {
                "faq_id": doc.metadata.get("faq_id"),
                "category": doc.metadata.get("category")
            }
            for doc in filtered_docs
        ]

        logger.info(
            "chat_success session_id=%s sources_count=%s",
            session_id,
            len(sources)
        )

        return {
            "session_id": session_id,
            "answer": answer,
            "sources": sources
        }
