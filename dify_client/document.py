import json
from typing import Dict, List, Optional, Any, BinaryIO
from pathlib import Path
from .api_client import DifyAPIClient, APIError


class DocumentManager:
    """Manager for document operations."""
    
    def __init__(self, client: DifyAPIClient):
        self.client = client
    
    def list_documents(self, dataset_id: str, keyword: Optional[str] = None,
                      page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """List documents in a knowledge base."""
        params = {
            'page': page,
            'limit': limit
        }
        
        if keyword:
            params['keyword'] = keyword
        
        return self.client.get(f'/datasets/{dataset_id}/documents', params=params)
    
    def create_document_from_text(self, dataset_id: str, name: str, text: str,
                                 indexing_technique: str = 'high_quality',
                                 doc_form: Optional[str] = None,
                                 doc_language: Optional[str] = None,
                                 process_rule: Optional[Dict[str, Any]] = None,
                                 retrieval_model: Optional[Dict[str, Any]] = None,
                                 embedding_model: Optional[str] = None,
                                 embedding_model_provider: Optional[str] = None) -> Dict[str, Any]:
        """Create a document from text."""
        data = {
            'name': name,
            'text': text,
            'indexing_technique': indexing_technique
        }
        
        if doc_form:
            data['doc_form'] = doc_form
        
        if doc_language:
            data['doc_language'] = doc_language
        
        if process_rule:
            data['process_rule'] = process_rule
        else:
            # Default to automatic mode
            data['process_rule'] = {'mode': 'automatic'}
        
        # Add optional parameters for first upload
        if retrieval_model:
            data['retrieval_model'] = retrieval_model
        
        if embedding_model:
            data['embedding_model'] = embedding_model
        
        if embedding_model_provider:
            data['embedding_model_provider'] = embedding_model_provider
        
        return self.client.post(f'/datasets/{dataset_id}/document/create-by-text', data=data)
    
    def create_document_from_file(self, dataset_id: str, file_path: str,
                                 original_document_id: Optional[str] = None,
                                 indexing_technique: str = 'high_quality',
                                 doc_form: Optional[str] = None,
                                 doc_language: Optional[str] = None,
                                 process_rule: Optional[Dict[str, Any]] = None,
                                 retrieval_model: Optional[Dict[str, Any]] = None,
                                 embedding_model: Optional[str] = None,
                                 embedding_model_provider: Optional[str] = None) -> Dict[str, Any]:
        """Create a document from a file."""
        # Prepare data as JSON string for multipart upload
        data_dict = {
            'indexing_technique': indexing_technique
        }
        
        if original_document_id:
            data_dict['original_document_id'] = original_document_id
        
        if doc_form:
            data_dict['doc_form'] = doc_form
        
        if doc_language:
            data_dict['doc_language'] = doc_language
        
        if process_rule:
            data_dict['process_rule'] = process_rule
        else:
            # Default to automatic mode
            data_dict['process_rule'] = {'mode': 'automatic'}
        
        # Add optional parameters for first upload
        if retrieval_model:
            data_dict['retrieval_model'] = retrieval_model
        
        if embedding_model:
            data_dict['embedding_model'] = embedding_model
        
        if embedding_model_provider:
            data_dict['embedding_model_provider'] = embedding_model_provider
        
        # Convert to JSON string
        data_json = json.dumps(data_dict)
        
        # Prepare files for upload
        with open(file_path, 'rb') as f:
            files = {
                'data': ('data', data_json, 'text/plain'),
                'file': (Path(file_path).name, f, 'application/octet-stream')
            }
            
            return self.client.post(f'/datasets/{dataset_id}/document/create-by-file', files=files)
    
    def update_document_by_text(self, dataset_id: str, document_id: str,
                               name: Optional[str] = None,
                               text: Optional[str] = None,
                               process_rule: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update a document with text."""
        data = {}
        
        if name:
            data['name'] = name
        
        if text:
            data['text'] = text
        
        if process_rule:
            data['process_rule'] = process_rule
        
        return self.client.post(f'/datasets/{dataset_id}/documents/{document_id}/update-by-text', data=data)
    
    def update_document_by_file(self, dataset_id: str, document_id: str,
                               file_path: str,
                               name: Optional[str] = None,
                               process_rule: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update a document with a file."""
        # Prepare data as JSON string for multipart upload
        data_dict = {}
        
        if name:
            data_dict['name'] = name
        
        if process_rule:
            data_dict['process_rule'] = process_rule
        
        # Convert to JSON string
        data_json = json.dumps(data_dict)
        
        # Prepare files for upload
        with open(file_path, 'rb') as f:
            files = {
                'data': ('data', data_json, 'text/plain'),
                'file': (Path(file_path).name, f, 'application/octet-stream')
            }
            
            return self.client.post(f'/datasets/{dataset_id}/documents/{document_id}/update-by-file', files=files)
    
    def delete_document(self, dataset_id: str, document_id: str) -> Dict[str, Any]:
        """Delete a document."""
        return self.client.delete(f'/datasets/{dataset_id}/documents/{document_id}')
    
    def get_document_indexing_status(self, dataset_id: str, batch: str) -> Dict[str, Any]:
        """Get document embedding status."""
        return self.client.get(f'/datasets/{dataset_id}/documents/{batch}/indexing-status')
    
    def get_upload_file(self, dataset_id: str, document_id: str) -> Dict[str, Any]:
        """Get uploaded file information."""
        return self.client.get(f'/datasets/{dataset_id}/documents/{document_id}/upload-file')
    
    def create_process_rule(self, mode: str = 'automatic',
                           pre_processing_rules: Optional[List[Dict[str, Any]]] = None,
                           segmentation: Optional[Dict[str, Any]] = None,
                           parent_mode: Optional[str] = None,
                           subchunk_segmentation: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Helper to create process rule configuration."""
        process_rule = {'mode': mode}
        
        if mode == 'custom':
            rules = {}
            
            if pre_processing_rules:
                rules['pre_processing_rules'] = pre_processing_rules
            else:
                # Default preprocessing rules
                rules['pre_processing_rules'] = [
                    {'id': 'remove_extra_spaces', 'enabled': True},
                    {'id': 'remove_urls_emails', 'enabled': True}
                ]
            
            if segmentation:
                rules['segmentation'] = segmentation
            else:
                # Default segmentation
                rules['segmentation'] = {
                    'separator': '\\n',
                    'max_tokens': 1000
                }
            
            process_rule['rules'] = rules
        
        elif mode == 'hierarchical':
            rules = {}
            
            if parent_mode:
                rules['parent_mode'] = parent_mode
            
            if subchunk_segmentation:
                rules['subchunk_segmentation'] = subchunk_segmentation
            
            if rules:
                process_rule['rules'] = rules
        
        return process_rule