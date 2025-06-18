# Dify Knowledge Base Client

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An interactive Python client for managing [Dify](https://dify.ai/) Knowledge Bases through the API. This client provides a user-friendly command-line interface to interact with all features of the Dify Knowledge API.

<img src="https://github.com/user-attachments/assets/placeholder-demo.gif" alt="Demo" width="600">

## ✨ Features

- **🗄️ Knowledge Base Management**: Create, list, update, and delete knowledge bases
- **📄 Document Management**: Upload documents from text or files, update, and delete
- **🔍 Advanced Search**: Multiple search methods (semantic, keyword, full-text, hybrid)
- **📊 Segment Management**: Fine-grained control over document chunks
- **🏷️ Metadata Support**: Custom metadata fields for enhanced organization
- **🎨 Rich CLI**: Beautiful terminal interface with autocomplete and visual feedback
- **🔌 Full API Coverage**: Complete implementation of Dify Knowledge API v1

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/DifyKnowledgeClient.git
cd DifyKnowledgeClient

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp .env.example .env
# Edit .env with your Dify API credentials
```

### Basic Usage

```bash
# Run the interactive CLI
python cli.py

# Or use as a package
pip install -e .
dify-client
```

## 📖 Documentation

### Interactive CLI

The CLI provides an intuitive menu-driven interface:

```
┌─────────────────────────────────────┐
│   Dify Knowledge Base Client        │
│   Interactive interface for         │
│   managing knowledge bases          │
└─────────────────────────────────────┘

Main Menu:
  1. Knowledge Base Management
  2. Document Management
  3. Segment/Chunk Management
  4. Search & Retrieval
  5. Metadata Management
  0. Exit

Select option:
```

### Programmatic Usage

```python
from dify_client.client import DifyClient

# Initialize client
client = DifyClient()  # Uses .env file

# Create a knowledge base
kb = client.knowledge_bases.create_dataset(
    name="My Knowledge Base",
    indexing_technique="high_quality"
)

# Upload a document
doc = client.documents.create_document_from_text(
    dataset_id=kb['id'],
    name="Introduction to AI",
    text="Artificial Intelligence is...",
    indexing_technique="high_quality"
)

# Search
results = client.retrieval.retrieve_chunks(
    dataset_id=kb['id'],
    query="What is AI?"
)
```

### Examples

Check the `examples/` directory for more detailed examples:
- `basic_usage.py` - Getting started with common operations
- `advanced_search.py` - Different search methods and configurations  
- `file_upload.py` - Uploading documents from files

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
DIFY_API_KEY=your-api-key-here
DIFY_BASE_URL=https://your-dify-instance.com/v1
```

### Indexing Techniques

- **high_quality**: Vector embedding for semantic search
- **economy**: Keyword-based inverted index

### Search Methods

- **semantic_search**: AI-powered similarity search
- **keyword_search**: Traditional keyword matching
- **full_text_search**: Complete text search
- **hybrid_search**: Combined semantic + keyword

## 🏗️ Project Structure

```
DifyKnowledgeClient/
├── dify_client/           # Core library
│   ├── api_client.py      # Base API client
│   ├── client.py          # Main client class
│   ├── knowledge_base.py  # KB operations
│   ├── document.py        # Document operations
│   ├── segment.py         # Segment operations
│   └── retrieval.py       # Search operations
├── examples/              # Usage examples
├── cli.py                 # Interactive CLI
├── requirements.txt       # Dependencies
└── setup.py              # Package setup
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Error**: Verify your API key in `.env`
2. **Connection Error**: Check your `DIFY_BASE_URL` 
3. **Import Error**: Ensure all dependencies are installed

### Getting Help

- 📋 [Report Issues](https://github.com/yourusername/DifyKnowledgeClient/issues)
- 💬 [Discussions](https://github.com/yourusername/DifyKnowledgeClient/discussions)
- 📚 [Dify Documentation](https://docs.dify.ai/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Dify](https://dify.ai/) team for the excellent Knowledge Base API
- Contributors and users of this client

---

<p align="center">Made with ❤️ for the Dify community</p>