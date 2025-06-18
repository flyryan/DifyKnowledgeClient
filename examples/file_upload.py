#!/usr/bin/env python3
"""
File upload examples for the Dify Knowledge Client.

Demonstrates uploading documents from files with different configurations.
"""

from pathlib import Path
from dify_client.client import DifyClient
from dify_client.api_client import APIError


def main():
    # Initialize the client
    client = DifyClient()
    
    # Get or create a knowledge base
    kb_id = input("Enter knowledge base ID (or 'new' to create one): ")
    
    if kb_id.lower() == 'new':
        try:
            kb = client.knowledge_bases.create_dataset(
                name="File Upload Example KB",
                description="Knowledge base for file upload examples",
                indexing_technique="high_quality",
                permission="only_me"
            )
            kb_id = kb['id']
            print(f"Created knowledge base: {kb['name']} (ID: {kb_id})")
        except APIError as e:
            print(f"Error creating knowledge base: {e}")
            return
    
    # Example 1: Upload a text file
    print("\n=== Uploading Text File ===")
    
    # Create a sample text file
    sample_file = Path("sample_document.txt")
    sample_file.write_text("""
    Introduction to Machine Learning
    
    Machine learning is a subset of artificial intelligence that focuses on
    building systems that learn from data. Instead of being explicitly programmed,
    these systems improve their performance through experience.
    
    Types of Machine Learning:
    1. Supervised Learning - Learning from labeled examples
    2. Unsupervised Learning - Finding patterns in unlabeled data
    3. Reinforcement Learning - Learning through interaction and feedback
    
    Applications include image recognition, natural language processing,
    recommendation systems, and autonomous vehicles.
    """)
    
    try:
        # Upload with automatic processing
        doc = client.documents.create_document_from_file(
            dataset_id=kb_id,
            file_path=str(sample_file),
            indexing_technique="high_quality",
            process_rule={'mode': 'automatic'}
        )
        print(f"Uploaded: {doc['document']['name']} (ID: {doc['document']['id']})")
        print(f"Status: {doc['document']['indexing_status']}")
        
        if doc.get('batch'):
            print(f"Batch ID for status tracking: {doc['batch']}")
    except APIError as e:
        print(f"Error uploading file: {e}")
    
    # Example 2: Upload with custom segmentation
    print("\n=== Uploading with Custom Segmentation ===")
    
    # Create another sample file
    custom_file = Path("custom_segmentation.txt")
    custom_file.write_text("""
    Chapter 1: Introduction
    ###
    This is the first chapter about getting started with AI.
    It covers basic concepts and terminology.
    ###
    Chapter 2: Deep Learning
    ###
    Deep learning uses neural networks with multiple layers.
    These networks can learn complex patterns from data.
    ###
    Chapter 3: Applications
    ###
    AI is used in healthcare, finance, and transportation.
    The future holds even more possibilities.
    """)
    
    try:
        # Create custom process rule
        process_rule = client.documents.create_process_rule(
            mode="custom",
            segmentation={
                'separator': '###',
                'max_tokens': 500
            }
        )
        
        doc = client.documents.create_document_from_file(
            dataset_id=kb_id,
            file_path=str(custom_file),
            indexing_technique="high_quality",
            process_rule=process_rule
        )
        print(f"Uploaded with custom segmentation: {doc['document']['name']}")
    except APIError as e:
        print(f"Error: {e}")
    
    # Example 3: Upload in Q&A mode
    print("\n=== Uploading in Q&A Mode ===")
    
    qa_file = Path("qa_document.txt")
    qa_file.write_text("""
    Q: What is artificial intelligence?
    A: Artificial intelligence (AI) is the simulation of human intelligence in machines that are programmed to think and learn like humans.
    
    Q: What are the main types of AI?
    A: The main types are: Narrow AI (designed for specific tasks), General AI (human-level intelligence), and Super AI (surpassing human intelligence).
    
    Q: How does machine learning relate to AI?
    A: Machine learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed.
    """)
    
    try:
        doc = client.documents.create_document_from_file(
            dataset_id=kb_id,
            file_path=str(qa_file),
            indexing_technique="high_quality",
            doc_form="qa_model",
            doc_language="English",
            process_rule={'mode': 'automatic'}
        )
        print(f"Uploaded in Q&A mode: {doc['document']['name']}")
    except APIError as e:
        print(f"Error: {e}")
    
    # Clean up sample files
    print("\n=== Cleanup ===")
    for file in [sample_file, custom_file, qa_file]:
        if file.exists():
            file.unlink()
            print(f"Deleted temporary file: {file}")
    
    print("\nFile upload examples completed!")
    print(f"Check your knowledge base (ID: {kb_id}) to see the uploaded documents.")


if __name__ == "__main__":
    main()