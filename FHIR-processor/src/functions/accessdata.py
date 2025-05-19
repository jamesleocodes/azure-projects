import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.helpers import AzureStorageHelper

storage_helper = AzureStorageHelper()
data = storage_helper.download_json("processed_patients.json")
print(data)