from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class Education:
    institution: str
    degree: str
    year: str


@dataclass
class Experience:
    company: str
    role: str
    duration: str


@dataclass
class ExtractedData:
    full_name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    education: List[Education] = field(default_factory=list)
    experience: List[Experience] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    raw_text: str = ""
    raw_skills: List[str] = field(default_factory=list)


@dataclass
class FraudFlag:
    check: str
    severity: str
    message: str


@dataclass
class FraudReport:
    fraud_risk_score: int
    risk_label: str
    flags: List[FraudFlag] = field(default_factory=list)


@dataclass
class HealthScore:
    total_score: int
    email_present: bool
    phone_present: bool
    education_detected: bool
    experience_detected: bool
    skills_count: int
    address_detected: bool
    suggestions: List[str] = field(default_factory=list)


@dataclass
class SubmissionResult:
    success: bool
    message: str
    submission_id: str
    timestamp: str
    payload: Dict[str, Any]


@dataclass
class EvaluationResult:
    resume_name: str
    field_name: str
    expected: str
    extracted: str
    correct: bool
    match_percentage: float = 0.0


@dataclass
class AccuracyReport:
    total_fields: int
    correct_fields: int
    accuracy_percentage: float
    field_wise_accuracy: Dict[str, float]
    results: List[EvaluationResult]
