import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from modules.schemas import SubmissionResult, ExtractedData


class DEETSubmissionSimulator:
    DEET_API_SCHEMA = {
        "full_name": "string",
        "email": "string",
        "phone": "string",
        "location": "string",
        "education": [
            {
                "institution": "string",
                "degree": "string",
                "year": "string"
            }
        ],
        "experience": [
            {
                "company": "string",
                "role": "string",
                "duration": "string"
            }
        ],
        "skills": ["string"]
    }
    
    def __init__(self):
        self.simulated_delay = 1.5
    
    def generate_payload(self, data: ExtractedData) -> Dict[str, Any]:
        payload = {
            "full_name": data.full_name,
            "email": data.email,
            "phone": data.phone,
            "location": data.location,
            "education": [
                {
                    "institution": edu.institution,
                    "degree": edu.degree,
                    "year": edu.year
                }
                for edu in data.education
            ],
            "experience": [
                {
                    "company": exp.company,
                    "role": exp.role,
                    "duration": exp.duration
                }
                for exp in data.experience
            ],
            "skills": data.skills,
            "registration_source": "DEET_SMART_REGISTRATION",
            "timestamp": datetime.now().isoformat()
        }
        
        return payload
    
    def validate_payload(self, payload: Dict[str, Any]) -> tuple:
        required_fields = ['full_name', 'email', 'phone']
        
        for field in required_fields:
            if not payload.get(field):
                return False, f"Missing required field: {field}"
        
        if not isinstance(payload.get('education'), list):
            return False, "Education must be a list"
        
        if not isinstance(payload.get('experience'), list):
            return False, "Experience must be a list"
        
        if not isinstance(payload.get('skills'), list):
            return False, "Skills must be a list"
        
        return True, "Payload valid"
    
    def submit(self, data: ExtractedData) -> SubmissionResult:
        import time
        time.sleep(self.simulated_delay)
        
        payload = self.generate_payload(data)
        
        is_valid, message = self.validate_payload(payload)
        
        if not is_valid:
            return SubmissionResult(
                success=False,
                message=message,
                submission_id="",
                timestamp=datetime.now().isoformat(),
                payload=payload
            )
        
        submission_id = f"DEET-{uuid.uuid4().hex[:12].upper()}"
        
        return SubmissionResult(
            success=True,
            message="Registration submitted successfully to DEET",
            submission_id=submission_id,
            timestamp=datetime.now().isoformat(),
            payload=payload
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return self.DEET_API_SCHEMA.copy()
    
    def get_schema_explanation(self) -> str:
        return """
DEET API Integration Guide:

The generated JSON payload matches DEET's required schema:

1. full_name (required): Candidate's full name as per official documents
2. email (required): Valid email address for communication
3. phone (required): 10-digit mobile number
4. location (optional): Current address/city
5. education (required): List of educational qualifications
   - institution: College/university name
   - degree: Degree obtained
   - year: Year of passing
6. experience (optional): Work experience details
   - company: Organization name
   - role: Job title
   - duration: Employment period
7. skills (optional): Technical and soft skills

To integrate with real DEET API:
- Replace the simulated endpoint with actual DEET API URL
- Add authentication headers (API key/OAuth token)
- Handle rate limiting and retries
- Implement proper error handling for API failures
"""


def submit_to_deet(data: ExtractedData) -> SubmissionResult:
    simulator = DEETSubmissionSimulator()
    return simulator.submit(data)


def generate_deet_payload(data: ExtractedData) -> Dict[str, Any]:
    simulator = DEETSubmissionSimulator()
    return simulator.generate_payload(data)
