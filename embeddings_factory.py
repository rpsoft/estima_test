"""
Embeddings factory module for creating embeddings instances based on configuration.
Supports both Ollama and OpenAI embeddings.
"""

from langchain.embeddings import OllamaEmbeddings, OpenAIEmbeddings
from config import config

def create_embeddings():
    """
    Create embeddings instance based on the configured provider.
    
    Returns:
        Embeddings instance (OllamaEmbeddings or OpenAIEmbeddings)
    """
    embeddings_config = config.get_embeddings_config()
    
    if embeddings_config["provider"] == "ollama":
        return OllamaEmbeddings(
            model=embeddings_config["model"],
            base_url=embeddings_config["base_url"]
        )
    elif embeddings_config["provider"] == "openai":
        return OpenAIEmbeddings(
            model=embeddings_config["model"],
            openai_api_key=embeddings_config["api_key"],
            openai_api_base=embeddings_config["base_url"],
            dimensions=embeddings_config.get("dimension")
        )
    else:
        raise ValueError(f"Unsupported embeddings provider: {embeddings_config['provider']}")

def get_embeddings_info():
    """
    Get information about the current embeddings configuration.
    
    Returns:
        dict: Embeddings configuration information
    """
    embeddings_config = config.get_embeddings_config()
    return {
        "provider": embeddings_config["provider"],
        "model": embeddings_config["model"],
        "dimension": embeddings_config.get("dimension", "default")
    }
