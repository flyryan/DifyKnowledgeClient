#!/usr/bin/env python3
"""
Basic usage examples for the Dify Knowledge Client.

This file demonstrates common operations using the programmatic API.
"""

from dify_client.client import DifyClient
from dify_client.api_client import APIError


def main():
    # Initialize the client (uses .env by default)
    client = DifyClient()
    
    # Example 1: List knowledge bases
    print("=== Listing Knowledge Bases ===")
    try:
        datasets = client.knowledge_bases.list_datasets(limit=5)
        for kb in datasets['data']:
            print(f"- {kb['name']} (ID: {kb['id']})")
            print(f"  Documents: {kb.get('document_count', 0)}, Words: {kb.get('word_count', 0)}")
    except APIError as e:
        print(f"Error listing knowledge bases: {e}")
    
    # Example 2: Create a knowledge base
    print("\n=== Creating a Knowledge Base ===")
    try:
        new_kb = client.knowledge_bases.create_dataset(
            name="Example Knowledge Base",
            description="Created via API example",
            indexing_technique="high_quality",
            permission="only_me"
        )
        print(f"Created: {new_kb['name']} (ID: {new_kb['id']})")
        kb_id = new_kb['id']
    except APIError as e:
        print(f"Error creating knowledge base: {e}")
        return
    
    # Example 3: Create a document from text
    print("\n=== Creating a Document ===")
    try:
        doc = client.documents.create_document_from_text(
            dataset_id=kb_id,
            name="Example Document",
            text="This is an example document created via the API. It contains sample text for testing.",
            indexing_technique="high_quality"
        )
        print(f"Created document: {doc['document']['name']} (ID: {doc['document']['id']})")
        doc_id = doc['document']['id']
    except APIError as e:
        print(f"Error creating document: {e}")
        return
    
    # Example 4: Search the knowledge base
    print("\n=== Searching Knowledge Base ===")
    try:
        # Wait a moment for indexing to complete
        import time
        print("Waiting for indexing to complete...")
        time.sleep(5)
        
        results = client.retrieval.retrieve_chunks(
            dataset_id=kb_id,
            query="example document"
        )
        
        print(f"Found {len(results.get('records', []))} results")
        for i, record in enumerate(results.get('records', [])[:3], 1):
            segment = record['segment']
            print(f"\nResult {i}:")
            print(f"- Content: {segment['content'][:100]}...")
            print(f"- Score: {record.get('score', 0):.6f}")
    except APIError as e:
        print(f"Error searching: {e}")
    
    # Example 5: Clean up (optional)
    print("\n=== Cleanup ===")
    if input("Delete the example knowledge base? (y/n): ").lower() == 'y':
        try:
            client.knowledge_bases.delete_dataset(kb_id)
            print("Knowledge base deleted successfully")
        except APIError as e:
            print(f"Error deleting knowledge base: {e}")


if __name__ == "__main__":
    main()