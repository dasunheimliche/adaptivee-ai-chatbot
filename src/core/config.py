from pydantic_settings import BaseSettings
from typing import List, Dict, Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Configuración de la aplicación utilizando Pydantic."""
    
    APP_NAME: str = "Adaptive AI Chatbot"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/adaptive_ai")
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")
    USE_SUPABASE: bool = os.getenv("USE_SUPABASE", "False").lower() == "true"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    AVAILABLE_AI_PROVIDERS: List[str] = []
    
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",
    ]
    
    class Config:
        case_sensitive = True
        
    def __init__(self, **data: Any):
        super().__init__(**data)
        
        # Configurar proveedores de IA disponibles basados en las claves API presentes
        if self.OPENAI_API_KEY:
            self.AVAILABLE_AI_PROVIDERS.append("openai")
        if self.ANTHROPIC_API_KEY:
            self.AVAILABLE_AI_PROVIDERS.append("anthropic")
        if self.GEMINI_API_KEY:
            self.AVAILABLE_AI_PROVIDERS.append("gemini")

settings = Settings()