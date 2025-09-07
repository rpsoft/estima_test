#!/usr/bin/env python3
"""
Test script to verify Estima configuration and model setup.
Run this script to check if your AI provider configuration is working correctly.
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment variables and configuration."""
    print("🔧 Testing Environment Configuration...")
    
    # Load environment variables
    load_dotenv()
    
    # Check required variables
    ai_provider = os.getenv("AI_PROVIDER", "ollama").lower()
    print(f"   AI Provider: {ai_provider}")
    
    if ai_provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            print("   ❌ OPENAI_API_KEY not set or using placeholder")
            return False
        else:
            print("   ✅ OpenAI API key configured")
    elif ai_provider == "ollama":
        ollama_url = os.getenv("OLLAMA_URL", "localhost:11434")
        print(f"   ✅ Ollama URL: {ollama_url}")
    else:
        print(f"   ❌ Invalid AI_PROVIDER: {ai_provider}")
        return False
    
    return True

def test_imports():
    """Test if all required modules can be imported."""
    print("\n📦 Testing Module Imports...")
    
    # Test core dependencies first
    core_deps = [
        ("langchain", "LangChain"),
        ("chromadb", "ChromaDB"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("ollama", "Ollama"),
        ("openai", "OpenAI"),
        ("dotenv", "python-dotenv"),
    ]
    
    for module, name in core_deps:
        try:
            __import__(module)
            print(f"   ✅ {name} imported")
        except ImportError as e:
            print(f"   ❌ Failed to import {name}: {e}")
            return False
    
    # Test our custom modules
    try:
        from config import config
        print("   ✅ Configuration module imported")
    except ImportError as e:
        print(f"   ❌ Failed to import config: {e}")
        return False
    
    try:
        from embeddings_factory import create_embeddings, get_embeddings_info
        print("   ✅ Embeddings factory imported")
    except ImportError as e:
        print(f"   ❌ Failed to import embeddings_factory: {e}")
        return False
    
    try:
        from generation_factory import create_chat_client, get_generation_info
        print("   ✅ Generation factory imported")
    except ImportError as e:
        print(f"   ❌ Failed to import generation_factory: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration object."""
    print("\n⚙️  Testing Configuration Object...")
    
    try:
        from config import config
        
        print(f"   Provider: {config.provider.value}")
        print(f"   Embeddings Model: {config.embeddings_model}")
        print(f"   Generation Model: {config.gen_model}")
        print(f"   Persist Directory: {config.persist_dir}")
        
        return True
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False

def test_embeddings():
    """Test embeddings creation."""
    print("\n🔍 Testing Embeddings...")
    
    try:
        from embeddings_factory import create_embeddings, get_embeddings_info
        
        embeddings_info = get_embeddings_info()
        print(f"   Provider: {embeddings_info['provider']}")
        print(f"   Model: {embeddings_info['model']}")
        
        # Try to create embeddings instance
        embeddings = create_embeddings()
        print("   ✅ Embeddings instance created successfully")
        
        return True
    except Exception as e:
        print(f"   ❌ Embeddings error: {e}")
        return False

def test_generation():
    """Test generation client creation."""
    print("\n💬 Testing Generation Client...")
    
    try:
        from generation_factory import create_chat_client, get_generation_info
        
        gen_info = get_generation_info()
        print(f"   Provider: {gen_info['provider']}")
        print(f"   Model: {gen_info['model']}")
        
        # Try to create chat client
        client = create_chat_client()
        print("   ✅ Chat client created successfully")
        
        return True
    except Exception as e:
        print(f"   ❌ Generation client error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Estima Configuration Test")
    print("=" * 50)
    
    tests = [
        test_environment,
        test_imports,
        test_configuration,
        test_embeddings,
        test_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print("   ⚠️  Test failed, but continuing...")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your configuration is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check your configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
