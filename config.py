"""
Configuration module for Estima - Medical Document Data Extraction System
Supports both Ollama and OpenAI services for embeddings and text generation.
"""

import os
from dotenv import load_dotenv
from enum import Enum

# Load environment variables
load_dotenv()

class ServiceProvider(Enum):
    """Available service providers for AI models."""
    OLLAMA = "ollama"
    OPENAI = "openai"

class ModelConfig:
    """Configuration class for managing AI model settings."""
    
    def __init__(self):
        self.provider = ServiceProvider(os.getenv("AI_PROVIDER", "ollama").lower())
        self.persist_dir = os.getenv("PERSIST_DIR", "./chroma_db9")
        
        # Embeddings configuration
        self.embeddings_model = os.getenv("EMBEDDINGS_MODEL")
        self.embeddings_dimension = int(os.getenv("EMBEDDINGS_DIMENSION", "1536"))
        
        # Generation configuration
        self.gen_model = os.getenv("GEN_MODEL")
        self.temperature = float(os.getenv("TEMPERATURE", "0.1"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
        
        # Service-specific URLs and API keys
        self.ollama_url = os.getenv("OLLAMA_URL", "localhost:11434")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        
        # Set default models based on provider
        self._set_default_models()
        
        # Validate configuration
        self._validate_config()
    
    def _set_default_models(self):
        """Set default models based on the selected provider."""
        if self.provider == ServiceProvider.OLLAMA:
            if not self.embeddings_model:
                self.embeddings_model = "oscardp96/medcpt-article"
            if not self.gen_model:
                self.gen_model = "gpt-oss"
        elif self.provider == ServiceProvider.OPENAI:
            if not self.embeddings_model:
                self.embeddings_model = "text-embedding-3-small"
            if not self.gen_model:
                self.gen_model = "gpt-4o-mini"
    
    def _validate_config(self):
        """Validate the configuration settings."""
        if self.provider == ServiceProvider.OPENAI:
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
        
        if not self.embeddings_model:
            raise ValueError("EMBEDDINGS_MODEL must be specified")
        
        if not self.gen_model:
            raise ValueError("GEN_MODEL must be specified")
    
    def get_embeddings_config(self):
        """Get embeddings configuration based on provider."""
        if self.provider == ServiceProvider.OLLAMA:
            return {
                "provider": "ollama",
                "model": self.embeddings_model,
                "base_url": self.ollama_url
            }
        elif self.provider == ServiceProvider.OPENAI:
            return {
                "provider": "openai",
                "model": self.embeddings_model,
                "api_key": self.openai_api_key,
                "base_url": self.openai_base_url,
                "dimension": self.embeddings_dimension
            }
    
    def get_generation_config(self):
        """Get generation configuration based on provider."""
        if self.provider == ServiceProvider.OLLAMA:
            return {
                "provider": "ollama",
                "model": self.gen_model,
                "base_url": self.ollama_url
            }
        elif self.provider == ServiceProvider.OPENAI:
            return {
                "provider": "openai",
                "model": self.gen_model,
                "api_key": self.openai_api_key,
                "base_url": self.openai_base_url,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
    
    def __str__(self):
        """String representation of the configuration."""
        return f"""ModelConfig:
  Provider: {self.provider.value}
  Embeddings Model: {self.embeddings_model}
  Generation Model: {self.gen_model}
  Persist Directory: {self.persist_dir}
  Temperature: {self.temperature}
  Max Tokens: {self.max_tokens}"""

# Global configuration instance
config = ModelConfig()
