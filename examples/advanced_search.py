#!/usr/bin/env python3
"""
Advanced search examples for the Dify Knowledge Client.

Demonstrates different search methods and configurations.
"""

from dify_client.client import DifyClient
from dify_client.api_client import APIError


def main():
    # Initialize the client
    client = DifyClient()
    
    # Assume we have a knowledge base ID (replace with your actual ID)
    kb_id = input("Enter knowledge base ID: ")
    
    # Example 1: Semantic Search
    print("\n=== Semantic Search Example ===")
    try:
        retrieval_model = client.retrieval.create_retrieval_model(
            search_method="semantic_search",
            top_k=5,
            score_threshold_enabled=True,
            score_threshold=0.5
        )
        
        results = client.retrieval.retrieve_chunks(
            dataset_id=kb_id,
            query="What is machine learning?",
            retrieval_model=retrieval_model
        )
        
        print(f"Found {len(results.get('records', []))} results with semantic search")
        for record in results.get('records', [])[:3]:
            print(f"- Score: {record['score']:.4f}")
            print(f"  Content: {record['segment']['content'][:100]}...")
    except APIError as e:
        print(f"Error: {e}")
    
    # Example 2: Keyword Search
    print("\n=== Keyword Search Example ===")
    try:
        retrieval_model = client.retrieval.create_retrieval_model(
            search_method="keyword_search",
            top_k=5
        )
        
        results = client.retrieval.retrieve_chunks(
            dataset_id=kb_id,
            query="machine learning",
            retrieval_model=retrieval_model
        )
        
        print(f"Found {len(results.get('records', []))} results with keyword search")
        for record in results.get('records', [])[:3]:
            print(f"- Score: {record['score']:.4f}")
            print(f"  Content: {record['segment']['content'][:100]}...")
    except APIError as e:
        print(f"Error: {e}")
    
    # Example 3: Hybrid Search with Reranking
    print("\n=== Hybrid Search with Reranking ===")
    try:
        # Note: You'll need to configure reranking models in your Dify instance
        retrieval_model = client.retrieval.create_retrieval_model(
            search_method="hybrid_search",
            weights=0.7,  # 70% semantic, 30% keyword
            top_k=10,
            reranking_enable=False  # Set to True if you have reranking configured
        )
        
        results = client.retrieval.retrieve_chunks(
            dataset_id=kb_id,
            query="explain neural networks in simple terms",
            retrieval_model=retrieval_model
        )
        
        print(f"Found {len(results.get('records', []))} results with hybrid search")
        for i, record in enumerate(results.get('records', [])[:3], 1):
            print(f"\nResult {i}:")
            print(f"- Document: {record['segment'].get('document', {}).get('name', 'Unknown')}")
            print(f"- Score: {record['score']:.4f}")
            print(f"- Content: {record['segment']['content'][:150]}...")
    except APIError as e:
        print(f"Error: {e}")
    
    # Example 4: Full-text Search
    print("\n=== Full-text Search Example ===")
    try:
        retrieval_model = client.retrieval.create_retrieval_model(
            search_method="full_text_search",
            top_k=5
        )
        
        results = client.retrieval.retrieve_chunks(
            dataset_id=kb_id,
            query="neural network architecture layers",
            retrieval_model=retrieval_model
        )
        
        print(f"Found {len(results.get('records', []))} results with full-text search")
        for record in results.get('records', [])[:3]:
            print(f"- Score: {record['score']:.4f}")
            print(f"  Keywords: {', '.join(record['segment'].get('keywords', [])[:5])}")
    except APIError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()