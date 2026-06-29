"""Configuration helpers for the capstone project.

Never hard-code API keys in source code. Put secrets in a local `.env` file.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    chat_model: str = os.getenv("CHAT_MODEL", "gpt-4o-mini")
    embed_model: str = os.getenv("EMBED_MODEL", "text-embedding-3-small")

    vector_db: str = os.getenv("VECTOR_DB", "chroma")
    chroma_dir: str = os.getenv("CHROMA_DIR", "./chroma_db")
    chroma_collection: str = os.getenv("CHROMA_COLLECTION", "capstone_research_corpus")

    neo4j_uri: str = os.getenv("NEO4J_URI", "")
    neo4j_username: str = os.getenv("NEO4J_USERNAME", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "")
    neo4j_database: str = os.getenv("NEO4J_DATABASE", "neo4j")


settings = Settings()


def require_openai_key() -> None:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Copy .env.example to .env and set your key.")
