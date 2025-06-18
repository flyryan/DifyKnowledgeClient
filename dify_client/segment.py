from typing import Dict, List, Optional, Any
from .api_client import DifyAPIClient, APIError


class SegmentManager:
    """Manager for segment/chunk operations."""
    
    def __init__(self, client: DifyAPIClient):
        self.client = client
    
    def add_segments(self, dataset_id: str, document_id: str,
                    segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add chunks to a document."""
        data = {'segments': segments}
        return self.client.post(f'/datasets/{dataset_id}/documents/{document_id}/segments', data=data)
    
    def list_segments(self, dataset_id: str, document_id: str,
                     keyword: Optional[str] = None,
                     status: Optional[str] = None,
                     page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """Get chunks from a document."""
        params = {
            'page': page,
            'limit': limit
        }
        
        if keyword:
            params['keyword'] = keyword
        
        if status:
            params['status'] = status
        
        return self.client.get(f'/datasets/{dataset_id}/documents/{document_id}/segments', params=params)
    
    def update_segment(self, dataset_id: str, document_id: str, segment_id: str,
                      content: Optional[str] = None,
                      answer: Optional[str] = None,
                      keywords: Optional[List[str]] = None,
                      enabled: Optional[bool] = None,
                      regenerate_child_chunks: Optional[bool] = None) -> Dict[str, Any]:
        """Update a chunk in a document."""
        segment_data = {}
        
        if content is not None:
            segment_data['content'] = content
        
        if answer is not None:
            segment_data['answer'] = answer
        
        if keywords is not None:
            segment_data['keywords'] = keywords
        
        if enabled is not None:
            segment_data['enabled'] = enabled
        
        if regenerate_child_chunks is not None:
            segment_data['regenerate_child_chunks'] = regenerate_child_chunks
        
        data = {'segment': segment_data}
        return self.client.post(f'/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}', data=data)
    
    def delete_segment(self, dataset_id: str, document_id: str, segment_id: str) -> Dict[str, Any]:
        """Delete a chunk in a document."""
        return self.client.delete(f'/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}')
    
    def create_child_chunk(self, dataset_id: str, document_id: str, segment_id: str,
                          content: str) -> Dict[str, Any]:
        """Create a child chunk."""
        data = {'content': content}
        return self.client.post(f'/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks', data=data)
    
    def list_child_chunks(self, dataset_id: str, document_id: str, segment_id: str,
                         keyword: Optional[str] = None,
                         page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """Get child chunks."""
        params = {
            'page': page,
            'limit': limit
        }
        
        if keyword:
            params['keyword'] = keyword
        
        return self.client.get(f'/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks', params=params)
    
    def update_child_chunk(self, dataset_id: str, document_id: str, segment_id: str,
                          child_chunk_id: str, content: str) -> Dict[str, Any]:
        """Update a child chunk."""
        data = {'content': content}
        return self.client.patch(f'/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks/{child_chunk_id}', data=data)
    
    def delete_child_chunk(self, dataset_id: str, document_id: str, segment_id: str,
                          child_chunk_id: str) -> Dict[str, Any]:
        """Delete a child chunk."""
        return self.client.delete(f'/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks/{child_chunk_id}')
    
    def create_segment(self, content: str, answer: Optional[str] = None,
                      keywords: Optional[List[str]] = None) -> Dict[str, Any]:
        """Helper to create a segment structure."""
        segment = {'content': content}
        
        if answer:
            segment['answer'] = answer
        
        if keywords:
            segment['keywords'] = keywords
        
        return segment