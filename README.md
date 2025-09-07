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
- Ollama (running locally or remotely)
- Required Ollama models:
  - `oscardp96/medcpt-article` (for embeddings)
  - `gpt-oss` (for text generation)

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
   pip install langchain chromadb ollama pdfplumber python-dotenv pandas
   ```

4. **Set up Ollama**:
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull required models
   ollama pull oscardp96/medcpt-article
   ollama pull gpt-oss
   ```

5. **Environment Configuration**:
   Create a `.env` file in the project root:
   ```env
   PERSIST_DIR=./chroma_db8
   EMBEDDINGS_MODEL=oscardp96/medcpt-article
   GEN_MODEL=gpt-oss
   OLLAMA_URL=localhost:11434
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
- `PERSIST_DIR`: Directory for ChromaDB persistence (default: `./chroma_db`)
- `EMBEDDINGS_MODEL`: Ollama model for embeddings (default: `oscardp96/medcpt-article`)
- `GEN_MODEL`: Ollama model for text generation (default: `gpt-oss`)
- `OLLAMA_URL`: Ollama server URL (default: `localhost:11434`)

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

## Support

For issues and questions, please contact [jesus.rodriguezperez@datasky.uk].
