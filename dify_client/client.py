from typing import Optional
from .api_client import DifyAPIClient
from .knowledge_base import KnowledgeBaseManager
from .document import DocumentManager
from .segment import SegmentManager
from .retrieval import RetrievalManager


class DifyClient:
    """Main client for interacting with Dify Knowledge API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize the Dify client.
        
        Args:
            api_key: API key for authentication. If not provided, will use DIFY_API_KEY env var.
            base_url: Base URL for the API. If not provided, will use DIFY_BASE_URL env var.
        """
        self.api_client = DifyAPIClient(api_key, base_url)
        
        # Initialize managers
        self.knowledge_bases = KnowledgeBaseManager(self.api_client)
        self.documents = DocumentManager(self.api_client)
        self.segments = SegmentManager(self.api_client)
        self.retrieval = RetrievalManager(self.api_client)