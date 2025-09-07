"""
Generation factory module for creating chat completion clients based on configuration.
Supports both Ollama and OpenAI chat completions.
"""

import ollama
import openai
from config import config

class ChatResponse:
    """Wrapper class to standardize response format across providers."""
    
    def __init__(self, content, provider, model):
        self.content = content
        self.provider = provider
        self.model = model
    
    def __str__(self):
        return self.content

def create_chat_client():
    """
    Create chat client based on the configured provider.
    
    Returns:
        Chat client instance
    """
    gen_config = config.get_generation_config()
    
    if gen_config["provider"] == "ollama":
        return OllamaChatClient(gen_config)
    elif gen_config["provider"] == "openai":
        return OpenAIChatClient(gen_config)
    else:
        raise ValueError(f"Unsupported generation provider: {gen_config['provider']}")

class OllamaChatClient:
    """Ollama chat client wrapper."""
    
    def __init__(self, config):
        self.config = config
        self.client = ollama.Client(host=config["base_url"])
    
    def chat(self, messages):
        """
        Send chat completion request to Ollama.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            ChatResponse object
        """
        response = self.client.chat(
            model=self.config["model"],
            messages=messages
        )
        
        return ChatResponse(
            content=response["message"]["content"],
            provider="ollama",
            model=self.config["model"]
        )

class OpenAIChatClient:
    """OpenAI chat client wrapper."""
    
    def __init__(self, config):
        self.config = config
        self.client = openai.OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"]
        )
    
    def chat(self, messages):
        """
        Send chat completion request to OpenAI.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            ChatResponse object
        """
        response = self.client.chat.completions.create(
            model=self.config["model"],
            messages=messages,
            temperature=self.config.get("temperature", 0.1),
            max_tokens=self.config.get("max_tokens", 2000)
        )
        
        return ChatResponse(
            content=response.choices[0].message.content,
            provider="openai",
            model=self.config["model"]
        )

def get_generation_info():
    """
    Get information about the current generation configuration.
    
    Returns:
        dict: Generation configuration information
    """
    gen_config = config.get_generation_config()
    return {
        "provider": gen_config["provider"],
        "model": gen_config["model"],
        "temperature": gen_config.get("temperature", "default"),
        "max_tokens": gen_config.get("max_tokens", "default")
    }
