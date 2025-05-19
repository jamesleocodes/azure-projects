import os
import sys
import logging
from typing import Dict, List
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.helpers import AzureStorageHelper, FHIRHelper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_patient_data(patient: Dict) -> Dict:
    """Process a single patient resource."""
    try:
        # Extract basic information
        return {
            'patient_id': patient.get('id'),
            'name': _extract_name(patient),
            'gender': patient.get('gender'),
            'birth_date': patient.get('birthDate'),
            'address': _extract_address(patient),
            'processed_date': datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error processing patient {patient.get('id')}: {str(e)}")
        return None

def _extract_name(patient: Dict) -> str:
    """Extract patient name."""
    names = patient.get('name', [])
    if names:
        name = names[0]
        given = ' '.join(name.get('given', []))
        family = name.get('family', '')
        return f"{given} {family}".strip()
    return ''

def _extract_address(patient: Dict) -> str:
    """Extract patient address."""
    addresses = patient.get('address', [])
    if addresses:
        address = addresses[0]
        components = []
        
        # Handle line as a list
        if 'line' in address:
            components.extend(address['line'])
            
        # Add other address components
        for field in ['city', 'state', 'postalCode']:
            if field in address:
                components.append(address[field])
                
        return ', '.join(filter(None, components))
    return ''

def main():
    # Initialize helpers
    storage_helper = AzureStorageHelper()
    fhir_helper = FHIRHelper()
    
    try:
        # Example patient data
        sample_patients = [
            {
                "resourceType": "Patient",
                "id": "pat1",
                "name": [{"family": "Smith", "given": ["John"]}],
                "gender": "male",
                "birthDate": "1974-12-25",
                "address": [{
                    "line": ["123 Main St"],
                    "city": "Anytown",
                    "state": "CA",
                    "postalCode": "12345"
                }]
            },
            {
                "resourceType": "Patient",
                "id": "pat2",
                "name": [{"family": "Johnson", "given": ["Sarah"]}],
                "gender": "female",
                "birthDate": "1985-06-15",
                "address": [{
                    "line": ["456 Oak Ave"],
                    "city": "Somewhere",
                    "state": "NY",
                    "postalCode": "67890"
                }]
            }
        ]
        
        # Process each patient
        processed_patients = []
        for patient in sample_patients:
            # Validate resource
            errors = fhir_helper.validate_resource(patient)
            if errors:
                logger.warning(f"Validation errors for patient {patient.get('id')}: {errors}")
                continue
                
            # Format resource
            formatted_patient = fhir_helper.format_resource(patient)
            
            # Process patient data
            processed_data = process_patient_data(formatted_patient)
            if processed_data:
                processed_patients.append(processed_data)
        
        # Convert to DataFrame
        if processed_patients:
            df = pd.DataFrame(processed_patients)
            print("\nProcessed Patient Data:")
            print(df)
            
            # Save to Azure Blob Storage
            storage_helper.upload_json(processed_patients, "processed_patients.json")
            
            # Also save as CSV
            csv_data = df.to_csv(index=False)
            storage_helper.upload_json({"csv_data": csv_data}, "processed_patients.csv")
            
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main() 