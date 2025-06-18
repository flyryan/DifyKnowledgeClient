from typing import Dict, List, Optional, Any
from .api_client import DifyAPIClient, APIError


class KnowledgeBaseManager:
    """Manager for knowledge base operations."""
    
    def __init__(self, client: DifyAPIClient):
        self.client = client
    
    def list_datasets(self, keyword: Optional[str] = None, tag_ids: Optional[List[str]] = None,
                     page: int = 1, limit: int = 20, include_all: bool = False) -> Dict[str, Any]:
        """List all knowledge bases."""
        params = {
            'page': page,
            'limit': limit,
            'include_all': include_all
        }
        
        if keyword:
            params['keyword'] = keyword
        
        if tag_ids:
            params['tag_ids'] = tag_ids
        
        return self.client.get('/datasets', params=params)
    
    def get_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """Get knowledge base details."""
        return self.client.get(f'/datasets/{dataset_id}')
    
    def create_dataset(self, name: str, description: Optional[str] = None,
                      indexing_technique: Optional[str] = None,
                      permission: str = 'only_me',
                      provider: str = 'vendor',
                      external_knowledge_api_id: Optional[str] = None,
                      external_knowledge_id: Optional[str] = None,
                      embedding_model: Optional[str] = None,
                      embedding_model_provider: Optional[str] = None,
                      retrieval_model: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new knowledge base."""
        data = {
            'name': name,
            'permission': permission,
            'provider': provider
        }
        
        if description:
            data['description'] = description
        
        if indexing_technique:
            data['indexing_technique'] = indexing_technique
        
        if external_knowledge_api_id:
            data['external_knowledge_api_id'] = external_knowledge_api_id
        
        if external_knowledge_id:
            data['external_knowledge_id'] = external_knowledge_id
        
        if embedding_model:
            data['embedding_model'] = embedding_model
        
        if embedding_model_provider:
            data['embedding_model_provider'] = embedding_model_provider
        
        if retrieval_model:
            data['retrieval_model'] = retrieval_model
        
        return self.client.post('/datasets', data=data)
    
    def update_dataset(self, dataset_id: str,
                      name: Optional[str] = None,
                      description: Optional[str] = None,
                      indexing_technique: Optional[str] = None,
                      permission: Optional[str] = None,
                      embedding_model_provider: Optional[str] = None,
                      embedding_model: Optional[str] = None,
                      retrieval_model: Optional[Dict[str, Any]] = None,
                      partial_member_list: Optional[List[str]] = None) -> Dict[str, Any]:
        """Update a knowledge base."""
        data = {}
        
        if name is not None:
            data['name'] = name
        
        if description is not None:
            data['description'] = description
        
        if indexing_technique is not None:
            data['indexing_technique'] = indexing_technique
        
        if permission is not None:
            data['permission'] = permission
        
        if embedding_model_provider is not None:
            data['embedding_model_provider'] = embedding_model_provider
        
        if embedding_model is not None:
            data['embedding_model'] = embedding_model
        
        if retrieval_model is not None:
            data['retrieval_model'] = retrieval_model
        
        if partial_member_list is not None:
            data['partial_member_list'] = partial_member_list
        
        return self.client.patch(f'/datasets/{dataset_id}', data=data)
    
    def delete_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """Delete a knowledge base."""
        return self.client.delete(f'/datasets/{dataset_id}')
    
    def get_available_embedding_models(self) -> Dict[str, Any]:
        """Get available embedding models."""
        return self.client.get('/workspaces/current/models/model-types/text-embedding')
    
    def create_retrieval_model(self, search_method: str = 'semantic_search',
                             reranking_enable: bool = False,
                             reranking_provider_name: Optional[str] = None,
                             reranking_model_name: Optional[str] = None,
                             weights: Optional[float] = None,
                             top_k: int = 2,
                             score_threshold_enabled: bool = False,
                             score_threshold: Optional[float] = None) -> Dict[str, Any]:
        """Helper to create retrieval model configuration."""
        retrieval_model = {
            'search_method': search_method,
            'reranking_enable': reranking_enable,
            'top_k': top_k,
            'score_threshold_enabled': score_threshold_enabled
        }
        
        if reranking_enable:
            retrieval_model['reranking_model'] = {
                'reranking_provider_name': reranking_provider_name or '',
                'reranking_model_name': reranking_model_name or ''
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