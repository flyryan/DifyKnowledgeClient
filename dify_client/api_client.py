import os
import json
from typing import Dict, List, Optional, Any, Tuple
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv

load_dotenv()


class DifyAPIClient:
    """Base API client for Dify Knowledge API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv('DIFY_API_KEY')
        self.base_url = (base_url or os.getenv('DIFY_BASE_URL', '')).rstrip('/')
        
        if not self.api_key:
            raise ValueError("API key is required. Set DIFY_API_KEY environment variable or pass it to the constructor.")
        
        if not self.base_url:
            raise ValueError("Base URL is required. Set DIFY_BASE_URL environment variable or pass it to the constructor.")
        
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to the API."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Handle 204 No Content responses
            if response.status_code == 204:
                return {"success": True}
            
            # Try to parse JSON response
            try:
                data = response.json()
            except json.JSONDecodeError:
                data = {"response": response.text}
            
            # Check for API errors
            if response.status_code >= 400:
                error_msg = data.get('message', f'API error: {response.status_code}')
                error_code = data.get('code', 'unknown_error')
                raise APIError(error_msg, error_code, response.status_code)
            
            return data
            
        except RequestException as e:
            raise APIError(f"Request failed: {str(e)}", "request_error", 0)
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request."""
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None, files: Optional[Dict] = None) -> Dict[str, Any]:
        """Make POST request."""
        kwargs = {}
        
        if files:
            # For file uploads, don't set Content-Type header (let requests set it)
            headers = self.session.headers.copy()
            headers.pop('Content-Type', None)
            kwargs['headers'] = headers
            kwargs['files'] = files
            if data:
                kwargs['data'] = data
        else:
            kwargs['json'] = data
        
        return self._make_request('POST', endpoint, **kwargs)
    
    def patch(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make PATCH request."""
        return self._make_request('PATCH', endpoint, json=data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request."""
        return self._make_request('DELETE', endpoint)


class APIError(Exception):
    """Custom exception for API errors."""
    
    def __init__(self, message: str, code: str, status: int):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status
    
    def __str__(self):
        return f"[{self.code}] {self.message} (Status: {self.status})"