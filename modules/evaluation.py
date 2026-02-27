import json
from typing import Dict, List, Tuple, Optional
from modules.schemas import ExtractedData, EvaluationResult, AccuracyReport
from backend.nlp_extractor import extract_from_text
from difflib import SequenceMatcher


class AccuracyEvaluator:
    def __init__(self):
        self.test_cases = self._get_test_cases()
    
    def _get_test_cases(self) -> Dict[str, Dict]:
        return {
            "resume_1": {
                "expected": {
                    "email": "rahul.kumar@example.com",
                    "phone": "9876543210",
                    "full_name": "Rahul Kumar",
                    "skills": ["python", "java", "react", "sql", "machine learning"],
                    "location": "Hyderabad"
                },
                "text": """
RAHUL KUMAR
Email: rahul.kumar@example.com
Phone: 9876543210
Hyderabad

EDUCATION:
B.Tech in Computer Science from IIT Hyderabad - 2019

EXPERIENCE:
Software Developer at TCS - 2 years
Python, Java, React, SQL, Machine Learning
"""
            },
            "resume_2": {
                "expected": {
                    "email": "priya.sharma@techmail.com",
                    "phone": "919987654321",
                    "full_name": "Priya Sharma",
                    "skills": ["python", "java", "javascript", "aws", "docker", "kubernetes"],
                    "location": "Bangalore"
                },
                "text": """
PRIYA SHARMA
priya.sharma@techmail.com
919987654321
Bangalore

Education:
BE Information Technology, RV College of Engineering, 2019
MBA, IIM Bangalore, 2021

Experience:
TCS Software Engineer - 2 years
Amazon Senior Software Developer - 3 years
Skills: Python, Java, JavaScript, AWS, Docker, Kubernetes
"""
            },
            "resume_3": {
                "expected": {
                    "email": "amit@yahoo.com",
                    "phone": "9445567890",
                    "full_name": "Amit Patel",
                    "skills": ["chemistry"],
                    "location": "Mumbai"
                },
                "text": """
AMIT PATEL
amit@yahoo.com
9445567890
Mumbai

Education:
B.Sc Chemistry from Mumbai University - 2018

Experience:
One year internship at local company
"""
            },
            "resume_4": {
                "expected": {
                    "email": "sneha@email.com",
                    "phone": "9555123456",
                    "full_name": "Sneha Reddy",
                    "skills": ["python", "django", "flask", "mysql", "git"],
                    "location": "Warangal"
                },
                "text": """
SNEHA REDDY
sneha@email.com
9555123456
Warangal

Education:
B.Tech in Computer Science from NIT Warangal - 2020

Experience:
Junior Developer at Startup - 1 year

Skills: Python, Django, Flask, MySQL, Git
"""
            },
            "resume_5": {
                "expected": {
                    "email": "rajesh.kumar@company.org",
                    "phone": "9000112233",
                    "full_name": "Rajesh Kumar",
                    "skills": ["data analysis", "excel", "powerbi", "tableau", "python"],
                    "location": "Karimnagar"
                },
                "text": """
RAJESH KUMAR
rajesh.kumar@company.org
9000112233
Karimnagar

Education:
B.Sc Statistics from Karimnagar University - 2017

Experience:
Data Analyst at Finance Corp - 3 years
Skills: Data Analysis, Excel, PowerBI, Tableau, Python
"""
            },
            "resume_6": {
                "expected": {
                    "email": "lavanya@startup.io",
                    "phone": "9988776655",
                    "full_name": "Lavanya",
                    "skills": ["ui/ux", "figma", "adobe xd", "photoshop"],
                    "location": "Secunderabad"
                },
                "text": """
LAVANYA
lavanya@startup.io
9988776655
Secunderabad

Education:
B.Des in UI/UX Design from Design Institute - 2021

Experience:
UI/UX Designer at Tech Startup - 2 years
Skills: UI/UX, Figma, Adobe XD, Photoshop
"""
            },
            "resume_7": {
                "expected": {
                    "email": "vijay.t@corp.net",
                    "phone": "9123456789",
                    "full_name": "Vijay Kumar",
                    "skills": ["c++", "python", "linux", "networking", "security"],
                    "location": "Nizamabad"
                },
                "text": """
VIJAY KUMAR
vijay.t@corp.net
9123456789
Nizamabad

Education:
B.Tech in Electronics from Nizamabad Institute - 2018

Experience:
System Engineer at IT Corp - 4 years
Skills: C++, Python, Linux, Networking, Security
"""
            },
            "resume_8": {
                "expected": {
                    "email": "divya.support@service.com",
                    "phone": "9876501234",
                    "full_name": "Divya",
                    "skills": ["customer service", "communication", "excel"],
                    "location": "Khammam"
                },
                "text": """
DIVYA
divya.support@service.com
9876501234
Khammam

Education:
B.A from Khammam College - 2019

Experience:
Customer Support Executive - 2 years
Skills: Customer Service, Communication, Excel
"""
            },
            "resume_9": {
                "expected": {
                    "email": "mahesh.dev@tech.co",
                    "phone": "9955112233",
                    "full_name": "Mahesh Babu",
                    "skills": ["javascript", "react", "nodejs", "mongodb", "express"],
                    "location": "Hyderabad"
                },
                "text": """
MAHESH BABU
mahesh.dev@tech.co
9955112233
Hyderabad

Education:
B.Tech in Computer Science from JNTU Hyderabad - 2020

Experience:
Full Stack Developer at Tech Company - 3 years
Skills: JavaScript, React, NodeJS, MongoDB, Express
"""
            },
            "resume_10": {
                "expected": {
                    "email": "farheen.ali@edu.org",
                    "phone": "9012345678",
                    "full_name": "Farheen Ali",
                    "skills": ["teaching", "communication", "microsoft office"],
                    "location": "Adilabad"
                },
                "text": """
FARHEEN ALI
farheen.ali@edu.org
9012345678
Adilabad

Education:
B.Ed from Adilabad College of Education - 2018

Experience:
Teacher at Government School - 3 years
Skills: Teaching, Communication, Microsoft Office
"""
            }
        }
    
    def add_test_case(self, name: str, text: str, expected: Dict):
        self.test_cases[name] = {
            "text": text,
            "expected": expected
        }
    
    def evaluate_single(self, test_name: str) -> List[EvaluationResult]:
        if test_name not in self.test_cases:
            return []
        
        test_case = self.test_cases[test_name]
        expected = test_case["expected"]
        text = test_case["text"]
        
        extracted = extract_from_text(text)
        
        results = []
        
        results.append(EvaluationResult(
            resume_name=test_name,
            field_name="email",
            expected=expected.get("email", ""),
            extracted=extracted.email,
            correct=expected.get("email", "").lower() == extracted.email.lower()
        ))
        
        results.append(EvaluationResult(
            resume_name=test_name,
            field_name="phone",
            expected=expected.get("phone", ""),
            extracted=extracted.phone,
            correct=expected.get("phone", "") == extracted.phone
        ))
        
        results.append(EvaluationResult(
            resume_name=test_name,
            field_name="full_name",
            expected=expected.get("full_name", ""),
            extracted=extracted.full_name,
            correct=self._fuzzy_match(expected.get("full_name", ""), extracted.full_name, 0.7)
        ))
        
        expected_skills = set([s.lower() for s in expected.get("skills", [])])
        extracted_skills = set([s.lower() for s in extracted.skills])
        skills_correct = len(expected_skills & extracted_skills) > 0
        results.append(EvaluationResult(
            resume_name=test_name,
            field_name="skills",
            expected=", ".join(sorted(expected_skills)),
            extracted=", ".join(sorted(extracted_skills)),
            correct=skills_correct
        ))
        
        results.append(EvaluationResult(
            resume_name=test_name,
            field_name="location",
            expected=expected.get("location", ""),
            extracted=extracted.location,
            correct=expected.get("location", "").lower() in extracted.location.lower() or 
                    extracted.location.lower() in expected.get("location", "").lower()
        ))
        
        return results
    
    def evaluate_all(self) -> AccuracyReport:
        all_results = []
        
        for test_name in self.test_cases:
            results = self.evaluate_single(test_name)
            all_results.extend(results)
        
        total = len(all_results)
        correct = sum(1 for r in all_results if r.correct)
        
        field_wise = {}
        for result in all_results:
            if result.field_name not in field_wise:
                field_wise[result.field_name] = {"total": 0, "correct": 0}
            field_wise[result.field_name]["total"] += 1
            if result.correct:
                field_wise[result.field_name]["correct"] += 1
        
        for field in field_wise:
            total_f = field_wise[field]["total"]
            correct_f = field_wise[field]["correct"]
            field_wise[field] = (correct_f / total_f * 100) if total_f > 0 else 0
        
        accuracy = (correct / total * 100) if total > 0 else 0
        
        return AccuracyReport(
            total_fields=total,
            correct_fields=correct,
            accuracy_percentage=accuracy,
            field_wise_accuracy=field_wise,
            results=all_results
        )
    
    def _fuzzy_match(self, str1: str, str2: str, threshold: float) -> bool:
        if not str1 or not str2:
            return False
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio() >= threshold
    
    def get_test_cases_summary(self) -> List[Dict]:
        summary = []
        for name, case in self.test_cases.items():
            summary.append({
                "name": name,
                "has_email": bool(case["expected"].get("email")),
                "has_phone": bool(case["expected"].get("phone")),
                "has_name": bool(case["expected"].get("full_name")),
                "skills_count": len(case["expected"].get("skills", []))
            })
        return summary


def run_evaluation() -> AccuracyReport:
    evaluator = AccuracyEvaluator()
    return evaluator.evaluate_all()


def get_evaluation_results() -> Tuple[List[EvaluationResult], AccuracyReport]:
    evaluator = AccuracyEvaluator()
    report = evaluator.evaluate_all()
    return report.results, report
