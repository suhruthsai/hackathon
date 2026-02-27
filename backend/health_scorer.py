from typing import List
from modules.schemas import HealthScore


class HealthScorer:
    def __init__(self):
        pass
    
    def calculate(
        self,
        email: str,
        phone: str,
        education_count: int,
        experience_count: int,
        skills: List[str],
        location: str
    ) -> HealthScore:
        score = 0
        suggestions = []
        
        email_present = bool(email)
        if email_present:
            score += 10
        else:
            suggestions.append("Add your email address for contact")
        
        phone_present = bool(phone)
        if phone_present:
            score += 10
        else:
            suggestions.append("Add your phone number for contact")
        
        education_detected = education_count > 0
        if education_detected:
            score += 20
        else:
            suggestions.append("Add your educational qualifications")
        
        experience_detected = experience_count > 0
        if experience_detected:
            score += 20
        else:
            suggestions.append("Add your work experience")
        
        skills_count = len(skills)
        if skills_count >= 5:
            score += 20
        elif skills_count > 0:
            score += int(skills_count * 4)
            suggestions.append(f"Add more skills (currently {skills_count}, recommend at least 5)")
        else:
            suggestions.append("Add your technical and soft skills")
        
        address_detected = bool(location)
        if address_detected:
            score += 20
        else:
            suggestions.append("Add your location/address")
        
        return HealthScore(
            total_score=score,
            email_present=email_present,
            phone_present=phone_present,
            education_detected=education_detected,
            experience_detected=experience_detected,
            skills_count=skills_count,
            address_detected=address_detected,
            suggestions=suggestions
        )


def calculate_health_score(
    email: str,
    phone: str,
    education_count: int,
    experience_count: int,
    skills: List[str],
    location: str
) -> HealthScore:
    scorer = HealthScorer()
    return scorer.calculate(
        email, phone, education_count, 
        experience_count, skills, location
    )
