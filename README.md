# Estima - Medical Document Data Extraction System

A Python-based system for extracting structured data from medical research documents using RAG (Retrieval-Augmented Generation) with Ollama and ChromaDB.

## Overview

This project extracts specific clinical trial data from medical research documents, particularly focusing on ulcerative colitis (UC) studies. It uses a combination of vector embeddings, similarity search, and large language models to identify and extract structured information from unstructured text documents.

## Features

- **Document Processing**: Converts PDF documents to text and creates searchable embeddings
- **RAG Pipeline**: Uses Retrieval-Augmented Generation for accurate data extraction
- **Structured Output**: Extracts data in JSON format and exports to CSV
- **Medical Focus**: Specialized for clinical trial data extraction including:
  - Patient demographics and baseline characteristics
  - Clinical outcomes and adverse events
  - Treatment arm information
  - Statistical measures (means, medians, proportions)

## Prerequisites

- Python 3.8+
- **Choose one of the following AI providers:**
  - **Ollama** (local, free): Running locally or remotely
    - Models: `oscardp96/medcpt-article` (embeddings), `gpt-oss` (generation)
  - **OpenAI** (cloud, paid): API key from [OpenAI Platform](https://platform.openai.com/api-keys)
    - Models: `text-embedding-3-small` (embeddings), `gpt-4o-mini` (generation)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd estima
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   # Install core dependencies
   pip install -r requirements.txt
   
   # Or for detailed version specifications:
   pip install -r requirements-detailed.txt
   
   # Verify installation:
   python check_dependencies.py
   ```

4. **Set up AI Provider** (choose one):

   **Option A: Ollama (Local)**
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull recommended models
   ollama pull oscardp96/medcpt-article
   ollama pull gpt-oss
   ```

   **Option B: OpenAI (Cloud)**
   - Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - No additional setup required

5. **Environment Configuration**:
   Copy `env.example` to `.env` and configure:
   ```bash
   cp env.example .env
   ```
   
   **For Ollama:**
   ```env
   AI_PROVIDER=ollama
   EMBEDDINGS_MODEL=oscardp96/medcpt-article
   GEN_MODEL=gpt-oss
   OLLAMA_URL=localhost:11434
   ```
   
   **For OpenAI:**
   ```env
   AI_PROVIDER=openai
   EMBEDDINGS_MODEL=text-embedding-3-small
   GEN_MODEL=gpt-4o-mini
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### 1. Document Processing
First, ensure your documents are in the `aws_raw/` directory as `.txt` files. The system will automatically process these documents and create embeddings.

### 2. Run Data Extraction
Execute the main extraction workflow:

```bash
python runExtraction.py
```

This will:
- Load or create the ChromaDB vector store
- Process all documents in `aws_raw/`
- Extract specified clinical trial data fields
- Save results to `extracted_data.json`

### 3. Format Output
Convert the extracted data to CSV format:

```python
import formatOutput
```

This creates `extracted_data.csv` with structured, flattened data.

## Data Fields Extracted

The system extracts the following clinical trial information:

### Baseline Characteristics
- Number of patients recruited by trial per treatment arm
- Patient gender (number, proportion)
- Age (mean/median with spread measures)
- Body mass index (mean/median with spread measures)
- Patient race (number/proportion by ethnicity)
- Disease duration (mean/median with spread, units)
- Location and extent of disease
- Number of acute UC episodes in the past year
- Adapted Mayo score and categories
- Previous medication use

### Clinical Outcomes
- Proportion of patients with clinical response (8-26 weeks)
- Proportion of patients with clinical and endoscopic response
- Proportion of patients with adverse events (AE)
- Proportion of patients with treatment-emergent adverse events (TEAE)

## Configuration

### Environment Variables

**Core Configuration:**
- `AI_PROVIDER`: Choose between `"ollama"` or `"openai"`
- `PERSIST_DIR`: Directory for ChromaDB persistence (default: `./chroma_db8`)

**Embeddings Configuration:**
- `EMBEDDINGS_MODEL`: Model for embeddings (auto-selected based on provider)
- `EMBEDDINGS_DIMENSION`: Embeddings dimension for OpenAI (default: `1536`)

**Generation Configuration:**
- `GEN_MODEL`: Model for text generation (auto-selected based on provider)
- `TEMPERATURE`: Generation temperature for OpenAI (default: `0.1`)
- `MAX_TOKENS`: Maximum tokens for OpenAI (default: `2000`)

**Ollama-specific:**
- `OLLAMA_URL`: Ollama server URL (default: `localhost:11434`)

**OpenAI-specific:**
- `OPENAI_API_KEY`: Your OpenAI API key (required for OpenAI)
- `OPENAI_BASE_URL`: OpenAI API base URL (default: `https://api.openai.com/v1`)

### Text Processing Parameters
- Chunk size: 1000 characters
- Chunk overlap: 200 characters
- Similarity search: Top 5 results (k=5)

## Output Format

The system generates two output files:

1. **`extracted_data.json`**: Raw extraction results with context
2. **`extracted_data.csv`**: Flattened, structured data for analysis

Each extracted field includes:
- Structured JSON data
- Explanation of extraction logic
- Source context from the document

## Model Recommendations

### Quick Setup Recommendations

**For Best Performance (OpenAI):**
```env
AI_PROVIDER=openai
EMBEDDINGS_MODEL=text-embedding-3-small
GEN_MODEL=gpt-4o-mini
```

**For Privacy/Local Use (Ollama):**
```env
AI_PROVIDER=ollama
EMBEDDINGS_MODEL=oscardp96/medcpt-article
GEN_MODEL=gpt-oss
```

**For Medical Documents:**
- Embeddings: `oscardp96/medcpt-article` (Ollama) or `text-embedding-3-small` (OpenAI)
- Generation: `gpt-oss` (Ollama) or `gpt-4o-mini` (OpenAI)

### Available Models

**Ollama Models:**
- Embeddings: `oscardp96/medcpt-article`, `nomic-embed-text`, `mxbai-embed-large`
- Generation: `gpt-oss`, `llama3.1:8b`, `mistral:7b`, `medllama2:7b`

**OpenAI Models:**
- Embeddings: `text-embedding-3-small`, `text-embedding-3-large`, `text-embedding-ada-002`
- Generation: `gpt-4o-mini`, `gpt-4o`, `gpt-3.5-turbo`

For detailed model comparisons, performance metrics, and cost analysis, see [`MODEL_RECOMMENDATIONS.md`](MODEL_RECOMMENDATIONS.md).

## Troubleshooting

### Dependency Issues

**Check Dependencies:**
```bash
# Run the dependency checker to identify issues:
python check_dependencies.py
```

**LangChain Import Errors:**
```bash
# If you get import errors, try installing specific LangChain components:
pip install langchain langchain-community langchain-core
```

**ChromaDB Issues:**
```bash
# If ChromaDB fails to install:
pip install chromadb --no-cache-dir
```

**OpenAI API Errors:**
- Verify your API key is correct and has sufficient credits
- Check if you're using the correct model names
- Ensure your OpenAI account has access to the models you're trying to use

**Ollama Connection Issues:**
- Ensure Ollama is running: `ollama serve`
- Check if models are installed: `ollama list`
- Verify the Ollama URL in your `.env` file

### Common Installation Problems

**Python Version Compatibility:**
- Ensure you're using Python 3.8 or higher
- Some packages may require Python 3.9+ for optimal performance

**Virtual Environment Issues:**
```bash
# If you encounter permission errors:
python -m venv venv --clear
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Memory Issues with Large Models:**
- Use smaller models for local Ollama setup
- Consider using OpenAI for memory-intensive operations
- Increase system RAM or use model quantization

## Support

For issues and questions, please contact [jesus.rodriguezperez@datasky.uk].
