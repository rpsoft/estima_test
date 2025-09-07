# Model Recommendations for Estima

This document provides recommendations for AI models to use with the Estima medical document extraction system, organized by provider and use case.

## Overview

The Estima system supports two AI providers:
- **Ollama**: Local, open-source models (free, private, requires local setup)
- **OpenAI**: Cloud-based models (paid, high performance, easy setup)

## Embeddings Models

Embeddings are used to create vector representations of document chunks for similarity search.

### Ollama Embeddings Models

| Model | Size | Specialization | Best For | Performance |
|-------|------|----------------|----------|-------------|
| `oscardp96/medcpt-article` | ~400MB | Medical/Clinical | Medical documents | ⭐⭐⭐⭐⭐ |
| `nomic-embed-text` | ~274MB | General | General text | ⭐⭐⭐⭐ |
| `mxbai-embed-large` | ~1.3GB | Multilingual | International docs | ⭐⭐⭐⭐ |
| `all-minilm` | ~23MB | General | Fast processing | ⭐⭐⭐ |

**Recommended**: `oscardp96/medcpt-article` - Specifically trained on medical literature and clinical text.

### OpenAI Embeddings Models

| Model | Dimensions | Cost/1K tokens | Specialization | Best For |
|-------|------------|----------------|----------------|----------|
| `text-embedding-3-small` | 1536 | $0.00002 | General | Cost-effective |
| `text-embedding-3-large` | 3072 | $0.00013 | General | High accuracy |
| `text-embedding-ada-002` | 1536 | $0.0001 | General | Legacy model |

**Recommended**: `text-embedding-3-small` - Best balance of cost and performance for medical text.

## Generation Models

Generation models are used to extract structured data from document chunks.

### Ollama Generation Models

| Model | Size | Specialization | Best For | Performance |
|-------|------|----------------|----------|-------------|
| `gpt-oss` | ~7GB | General | Structured output | ⭐⭐⭐⭐⭐ |
| `llama3.1:8b` | ~4.7GB | General | Balanced performance | ⭐⭐⭐⭐ |
| `llama3.1:70b` | ~40GB | General | High accuracy | ⭐⭐⭐⭐⭐ |
| `mistral:7b` | ~4.1GB | General | Fast inference | ⭐⭐⭐⭐ |
| `codellama:7b` | ~3.8GB | Code/Structured | JSON output | ⭐⭐⭐⭐ |
| `medllama2:7b` | ~4.1GB | Medical | Medical text | ⭐⭐⭐⭐⭐ |

**Recommended**: 
- `gpt-oss` - Excellent for structured JSON output
- `medllama2:7b` - Medical domain specialization (if available)

### OpenAI Generation Models

| Model | Context | Cost/1K tokens | Specialization | Best For |
|-------|---------|----------------|----------------|----------|
| `gpt-4o-mini` | 128K | $0.00015/$0.0006 | General | Cost-effective |
| `gpt-4o` | 128K | $0.005/$0.015 | General | High accuracy |
| `gpt-3.5-turbo` | 16K | $0.0005/$0.0015 | General | Legacy option |

**Recommended**: `gpt-4o-mini` - Best balance of cost, performance, and context length.

## Configuration Examples

### High-Performance Setup (OpenAI)
```env
AI_PROVIDER=openai
EMBEDDINGS_MODEL=text-embedding-3-small
GEN_MODEL=gpt-4o-mini
OPENAI_API_KEY=your_key_here
TEMPERATURE=0.1
MAX_TOKENS=2000
```

### Cost-Effective Setup (OpenAI)
```env
AI_PROVIDER=openai
EMBEDDINGS_MODEL=text-embedding-3-small
GEN_MODEL=gpt-3.5-turbo
OPENAI_API_KEY=your_key_here
TEMPERATURE=0.1
MAX_TOKENS=1500
```

### Local/Private Setup (Ollama)
```env
AI_PROVIDER=ollama
EMBEDDINGS_MODEL=oscardp96/medcpt-article
GEN_MODEL=gpt-oss
OLLAMA_URL=localhost:11434
```

### Medical-Focused Setup (Ollama)
```env
AI_PROVIDER=ollama
EMBEDDINGS_MODEL=oscardp96/medcpt-article
GEN_MODEL=medllama2:7b
OLLAMA_URL=localhost:11434
```

## Performance Considerations

### For Medical Document Extraction

1. **Embeddings**: Medical-specialized models perform significantly better
2. **Generation**: Models with strong JSON output capabilities are preferred
3. **Context**: Longer context windows help with complex medical documents

### Cost Optimization

1. **OpenAI**: Use `gpt-4o-mini` for most tasks, `gpt-4o` only for complex extractions
2. **Embeddings**: `text-embedding-3-small` provides best value
3. **Temperature**: Keep low (0.1) for consistent structured output

### Speed vs. Accuracy Trade-offs

| Setup | Speed | Accuracy | Cost | Privacy |
|-------|-------|----------|------|---------|
| Ollama (local) | Medium | High | Free | High |
| OpenAI (mini) | Fast | High | Low | Low |
| OpenAI (4o) | Medium | Highest | High | Low |

## Model Installation (Ollama)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull recommended models
ollama pull oscardp96/medcpt-article
ollama pull gpt-oss
ollama pull medllama2:7b  # If available

# Verify installation
ollama list
```

## Testing Your Setup

Create a test script to verify your configuration:

```python
from config import config
from embeddings_factory import get_embeddings_info
from generation_factory import get_generation_info

print("Configuration:")
print(config)
print("\nEmbeddings:", get_embeddings_info())
print("Generation:", get_generation_info())
```

## Troubleshooting

### Common Issues

1. **Ollama models not found**: Run `ollama pull <model-name>`
2. **OpenAI API errors**: Check API key and billing
3. **Memory issues**: Use smaller models or increase system RAM
4. **Slow performance**: Consider using OpenAI for faster inference

### Model-Specific Notes

- **oscardp96/medcpt-article**: May require specific Ollama version
- **gpt-oss**: Excellent for structured output, may need fine-tuning prompts
- **text-embedding-3-small**: Supports custom dimensions (up to 3072)
- **gpt-4o-mini**: Has rate limits, consider batching requests
