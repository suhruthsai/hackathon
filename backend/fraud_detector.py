import re
from typing import List, Optional
from modules.schemas import FraudReport, FraudFlag
from modules.config import FRAUD_KEYWORDS


class FraudDetector:
    def __init__(self):
        self.phone_pattern = re.compile(r'^(\+91)?[6-9]\d{9}$')
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def analyze(
        self,
        phone: str,
        email: str,
        skills: List[str],
        experience_count: int,
        raw_text: str,
        age: Optional[int] = None
    ) -> FraudReport:
        flags = []
        total_score = 0
        
        if phone:
            phone_score, phone_flag = self._check_phone(phone)
            total_score += phone_score
            if phone_flag:
                flags.append(phone_flag)
        
        if email:
            email_score, email_flag = self._check_email(email)
            total_score += email_score
            if email_flag:
                flags.append(email_flag)
        
        if skills:
            skills_score, skills_flag = self._check_skills(skills)
            total_score += skills_score
            if skills_flag:
                flags.append(skills_flag)
        
        if age and experience_count > 0:
            exp_score, exp_flag = self._check_experience_age(experience_count, age)
            total_score += exp_score
            if exp_flag:
                flags.append(exp_flag)
        
        if raw_text:
            keyword_score, keyword_flags = self._check_suspicious_keywords(raw_text)
            total_score += keyword_score
            flags.extend(keyword_flags)
        
        fraud_score = min(total_score, 100)
        
        risk_label = self._get_risk_label(fraud_score)
        
        return FraudReport(
            fraud_risk_score=fraud_score,
            risk_label=risk_label,
            flags=flags
        )
    
    def _check_phone(self, phone: str) -> tuple:
        clean_phone = re.sub(r'[^\d]', '', phone)
        
        if len(clean_phone) != 10:
            return 20, FraudFlag(
                check="phone_invalid",
                severity="high",
                message=f"Phone number must be 10 digits. Found: {phone}"
            )
        
        if not clean_phone.startswith(('6', '7', '8', '9')):
            return 15, FraudFlag(
                check="phone_invalid",
                severity="medium",
                message=f"Phone number should start with 6, 7, 8, or 9. Found: {phone}"
            )
        
        return 0, None
    
    def _check_email(self, email: str) -> tuple:
        if not self.email_pattern.match(email):
            return 15, FraudFlag(
                check="email_invalid",
                severity="medium",
                message=f"Invalid email format: {email}"
            )
        
        return 0, None
    
    def _check_skills(self, skills: List[str]) -> tuple:
        if len(skills) > 50:
            return 15, FraudFlag(
                check="excessive_skills",
                severity="medium",
                message=f"Excessive skills detected ({len(skills)}). This may indicate false information."
            )
        
        return 0, None
    
    def _check_experience_age(self, experience_years: int, age: int) -> tuple:
        if experience_years > age - 18 and age > 0:
            return 25, FraudFlag(
                check="experience_age_mismatch",
                severity="high",
                message=f"Experience ({experience_years} years) exceeds plausible age ({age} years)"
            )
        
        return 0, None
    
    def _check_suspicious_keywords(self, text: str) -> tuple:
        text_lower = text.lower()
        found_flags = []
        score = 0
        
        for keyword in FRAUD_KEYWORDS:
            if keyword.lower() in text_lower:
                score += 25
                found_flags.append(FraudFlag(
                    check="suspicious_keyword",
                    severity="high",
                    message=f"Suspicious keyword detected: '{keyword}'"
                ))
        
        return score, found_flags
    
    def _get_risk_label(self, score: int) -> str:
        if score < 25:
            return "Low"
        elif score < 50:
            return "Moderate"
        else:
            return "High"


def detect_fraud(
    phone: str,
    email: str,
    skills: List[str],
    experience_count: int,
    raw_text: str,
    age: Optional[int] = None
) -> FraudReport:
    detector = FraudDetector()
    return detector.analyze(phone, email, skills, experience_count, raw_text, age)
