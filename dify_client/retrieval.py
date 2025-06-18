from typing import Dict, List, Optional, Any
from .api_client import DifyAPIClient, APIError


class RetrievalManager:
    """Manager for retrieval and metadata operations."""
    
    def __init__(self, client: DifyAPIClient):
        self.client = client
    
    def retrieve_chunks(self, dataset_id: str, query: str,
                       retrieval_model: Optional[Dict[str, Any]] = None,
                       external_retrieval_model: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Retrieve chunks from a knowledge base."""
        data = {'query': query}
        
        if retrieval_model:
            data['retrieval_model'] = retrieval_model
        
        if external_retrieval_model:
            data['external_retrieval_model'] = external_retrieval_model
        
        return self.client.post(f'/datasets/{dataset_id}/retrieve', data=data)
    
    def create_metadata(self, dataset_id: str, metadata_type: str, name: str) -> Dict[str, Any]:
        """Create knowledge metadata."""
        data = {
            'type': metadata_type,
            'name': name
        }
        return self.client.post(f'/datasets/{dataset_id}/metadata', data=data)
    
    def update_metadata(self, dataset_id: str, metadata_id: str, name: str) -> Dict[str, Any]:
        """Update knowledge metadata."""
        data = {'name': name}
        return self.client.patch(f'/datasets/{dataset_id}/metadata/{metadata_id}', data=data)
    
    def delete_metadata(self, dataset_id: str, metadata_id: str) -> Dict[str, Any]:
        """Delete knowledge metadata."""
        return self.client.delete(f'/datasets/{dataset_id}/metadata/{metadata_id}')
    
    def list_metadata(self, dataset_id: str) -> Dict[str, Any]:
        """Get knowledge metadata list."""
        return self.client.get(f'/datasets/{dataset_id}/metadata')
    
    def toggle_builtin_metadata(self, dataset_id: str, action: str) -> Dict[str, Any]:
        """Enable or disable built-in metadata."""
        if action not in ['enable', 'disable']:
            raise ValueError("Action must be 'enable' or 'disable'")
        
        return self.client.post(f'/datasets/{dataset_id}/metadata/built-in/{action}')
    
    def update_documents_metadata(self, dataset_id: str,
                                 operation_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update documents metadata."""
        data = {'operation_data': operation_data}
        return self.client.post(f'/datasets/{dataset_id}/documents/metadata', data=data)
    
    def create_retrieval_model(self, search_method: str = 'semantic_search',
                             reranking_enable: bool = False,
                             reranking_provider_name: Optional[str] = None,
                             reranking_model_name: Optional[str] = None,
                             weights: Optional[float] = None,
                             top_k: int = 2,
                             score_threshold_enabled: bool = False,
                             score_threshold: Optional[float] = None) -> Dict[str, Any]:
        """Helper to create retrieval model configuration for retrieve operation."""
        retrieval_model = {
            'search_method': search_method,
            'reranking_enable': reranking_enable,
            'top_k': top_k,
            'score_threshold_enabled': score_threshold_enabled
        }
        
        if reranking_enable and reranking_provider_name and reranking_model_name:
            retrieval_model['reranking_mode'] = {
                'reranking_provider_name': reranking_provider_name,
                'reranking_model_name': reranking_model_name
            }
            retrieval_model['reranking_model'] = {
                'reranking_provider_name': reranking_provider_name,
                'reranking_model_name': reranking_model_name
            }
        else:
            retrieval_model['reranking_mode'] = None
            retrieval_model['reranking_model'] = {
                'reranking_provider_name': '',
                'reranking_model_name': ''
            }
        
        if weights is not None:
            retrieval_model['weights'] = weights
        else:
            retrieval_model['weights'] = None
        
        if score_threshold is not None:
            retrieval_model['score_threshold'] = score_threshold
        else:
            retrieval_model['score_threshold'] = None
        
        return retrieval_model