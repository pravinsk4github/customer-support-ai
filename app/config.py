from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Customer Support AI"
    app_env: str = "dev"

    database_url: str = "sqlite:///./support_ai.db"

    chroma_persist_directory: str = "./chroma_db"
    chroma_collection_name: str = "support_faqs"

    groq_api_key: str
    groq_model: str 
    embedding_model_name: str

    retrieval_k: int = 4
    retrieval_score_threshold: float
    retrieval_min_score_gap: float
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()