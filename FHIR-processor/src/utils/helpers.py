import logging
import json
import yaml
import os
from typing import Dict, Any, Optional
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AzureStorageHelper:
    def __init__(self):
        """Initialize Azure Storage helper with configuration."""
        self.config = self._load_config()
        self._setup_client()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            # Get the project root directory (2 levels up from this file)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            config_path = os.path.join(project_root, 'config.yaml')
            
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            raise

    def _setup_client(self):
        """Set up Azure Blob Storage client."""
        try:
            # Get connection string from environment variable
            connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
            if not connection_string:
                raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set")
                
            self.blob_service_client = BlobServiceClient.from_connection_string(
                connection_string
            )
            
            # Get container name from environment variable
            container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
            if not container_name:
                raise ValueError("AZURE_STORAGE_CONTAINER_NAME environment variable is not set")
                
            self.container_client = self.blob_service_client.get_container_client(container_name)
            
        except Exception as e:
            logger.error(f"Error setting up Azure Storage client: {str(e)}")
            raise

    def upload_json(self, data: Dict[str, Any], blob_name: str) -> None:
        """Upload JSON data to Azure Blob Storage."""
        try:
            json_data = json.dumps(data)
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.upload_blob(json_data, overwrite=True)
            logger.info(f"Successfully uploaded {blob_name}")
        except Exception as e:
            logger.error(f"Error uploading {blob_name}: {str(e)}")
            raise

    def download_json(self, blob_name: str) -> Optional[Dict[str, Any]]:
        """Download JSON data from Azure Blob Storage."""
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            download_stream = blob_client.download_blob()
            json_data = download_stream.readall()
            return json.loads(json_data)
        except Exception as e:
            logger.error(f"Error downloading {blob_name}: {str(e)}")
            return None

class FHIRHelper:
    @staticmethod
    def validate_resource(resource: Dict[str, Any]) -> list:
        """Validate FHIR resource for required fields."""
        errors = []
        required_fields = ['resourceType', 'id']
        
        for field in required_fields:
            if field not in resource:
                errors.append(f"Missing required field: {field}")
                
        return errors

    @staticmethod
    def format_resource(resource: Dict[str, Any]) -> Dict[str, Any]:
        """Format FHIR resource with metadata."""
        formatted = resource.copy()
        formatted['meta'] = {
            'versionId': '1',
            'lastUpdated': '2024-01-01T00:00:00Z'
        }
        return formatted

if __name__ == "__main__":
    # Example usage
    storage_helper = AzureStorageHelper()
    
    # Example data
    sample_data = {
        "resourceType": "Patient",
        "id": "123",
        "name": [{"family": "Smith", "given": ["John"]}]
    }
    
    # Upload data
    storage_helper.upload_json(sample_data, "sample_patient.json")
    
    # Download data
    downloaded_data = storage_helper.download_json("sample_patient.json")
    print("Downloaded data:", downloaded_data) 