# Azure-FHIR-Processor

A lightweight FHIR data processing solution using Azure's free tier services. This project demonstrates how to process and store FHIR-compliant data using Azure Blob Storage and Python. It includes sample scripts for data processing, validation, and access, with configuration via environment variables for security.

## Features
- Ingest, process, and validate FHIR resources (e.g., Patient)
- Store processed data as JSON and CSV in Azure Blob Storage
- Secure configuration using environment variables (`.env`)
- Example scripts for both uploading and accessing data

## Prerequisites
- Python 3.8+
- Azure account (with a Storage Account and Blob Container)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) (optional, for managing storage)

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd azure
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name
   AZURE_STORAGE_CONNECTION_STRING=your_connection_string
   AZURE_STORAGE_CONTAINER_NAME=your_container_name
   ```
   > **Note:** Never commit your `.env` file to version control.

4. **Edit `config.yaml` for non-sensitive settings**
   - Data processing and logging settings are configured here.

5. **(Optional) Create a container**
   - In Azure Portal: Go to your storage account > Containers > + Container
   - Or via CLI:
     ```bash
     az storage container create --name fhir-data --account-name <your_storage_account_name>
     ```

## Running the Example

### **Process and Upload Data**
From the project root, run:
```bash
python src/functions/process_fhir.py
```
- This will process sample FHIR Patient data and upload `processed_patients.json` and `processed_patients.csv` to your Azure Blob Storage container.

### **Access Data from Azure Blob Storage**
You can access your data in several ways:

#### **1. Azure Portal**
- Go to your storage account > Containers > [your container]
- Click on a file (e.g., `processed_patients.json`) and download

#### **2. Azure Storage Explorer**
- Download and install [Azure Storage Explorer](https://azure.microsoft.com/en-us/products/storage/storage-explorer/)
- Sign in and navigate to your container to view/download files

#### **3. Azure CLI**
```bash
az storage blob download \
  --account-name <your_storage_account_name> \
  --container-name <your_container_name> \
  --name processed_patients.json \
  --file ./processed_patients.json \
  --connection-string "<your_connection_string>"
```

#### **4. Python Script**
Example: `src/functions/accessdata.py`
```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.utils.helpers import AzureStorageHelper

storage_helper = AzureStorageHelper()
data = storage_helper.download_json("processed_patients.json")
print(data)
```
- Run from the project root:
  ```bash
  python src/functions/accessdata.py
  ```
- If you see `ModuleNotFoundError: No module named 'src'`, make sure you are running from the project root or adjust `sys.path` as shown above.

## Troubleshooting
- **ModuleNotFoundError:**
  - Run scripts from the project root, or
  - Add the project root to `sys.path` in your script, or
  - Set the `PYTHONPATH` environment variable when running scripts.
- **Config/Env Errors:**
  - Ensure your `.env` file is present and correct.
  - Ensure `config.yaml` is in the project root.
- **Azure Errors:**
  - Make sure your connection string and container name are correct.
  - Check your Azure Portal for storage account/container existence.

## Free Tier Limits
- **Azure Blob Storage:** 5GB storage, 20,000 transactions/month free
- Stay within these limits to avoid charges

## Security
- Never commit your `.env` file or connection strings to version control
- Use environment variables for all secrets

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## What is FHIR-Compliant Data?

FHIR (Fast Healthcare Interoperability Resources) is a standard for exchanging healthcare information electronically. FHIR-compliant data follows a structured format that makes it easy to share and integrate health records across different systems.

### Key Features of FHIR:
- **Resource-Based:** Data is organized into "resources" (e.g., Patient, Observation, Encounter).
- **JSON/XML Format:** Resources are typically stored in JSON or XML format.
- **RESTful API:** FHIR supports RESTful APIs for easy data access and updates.
- **Interoperability:** Designed to work seamlessly across different healthcare systems.

### Common FHIR Resource Types:
- **Patient:** Contains demographic and administrative information about a patient.
- **Observation:** Records clinical measurements, such as lab results or vital signs.
- **Encounter:** Represents a patient's visit or interaction with a healthcare provider.
- **Medication:** Details about prescribed medications.
- **Condition:** Diagnoses or health issues affecting the patient.

FHIR-compliant data ensures that healthcare information is standardized, secure, and easily accessible, making it ideal for modern healthcare applications. 