import re
from typing import List, Dict, Set, Optional
from modules.config import (
    EMAIL_PATTERN, PHONE_PATTERN, URL_PATTERN,
    DEGREE_KEYWORDS, EXPERIENCE_KEYWORDS, ALL_SKILLS
)
from modules.schemas import ExtractedData, Education, Experience


class NLPExtractor:
    def __init__(self):
        self.cities = [
            'hyderabad', 'secunderabad', 'bangalore', 'bengaluru', 'chennai', 'mumbai',
            'delhi', 'pune', 'kolkata', 'warangal', 'karimnagar', 'nizamabad', 'khammam',
            'adilabad', 'kakinada', 'vijayawada', 'visakhapatnam', 'tirupati', 'nellore',
            'gurgaon', 'noida', 'chandigarh', 'jaipur', 'ahmedabad', 'lucknow', 'coimbatore'
        ]
        
        self.name_patterns = [
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',
            r'([A-Z][a-z]+(?:\s+[A-Z]\.?\s*)?(?:\s+[A-Z][a-z]+)*)',
        ]
        
        self.company_patterns = [
            r'(?:at|@|in|with|working at|employed at|joined)\s+([A-Z][A-Za-z\s&]+?)(?:\s*[-|,]|$)',
            r'^([A-Z][A-Za-z\s&]+?)\s+(?:Pvt\.?|Ltd\.?|Inc\.?|Technologies?|Solutions?|Services?|Systems?|Consulting?)',
        ]
    
    def extract_all(self, text: str) -> ExtractedData:
        data = ExtractedData()
        data.raw_text = text
        
        data.email = self._extract_email(text)
        data.phone = self._extract_phone(text)
        
        data.full_name = self._extract_name(text)
        data.location = self._extract_location(text)
        
        data.education = self._extract_education(text)
        data.experience = self._extract_experience(text)
        
        data.skills = self._extract_skills(text)
        
        return data
    
    def _extract_email(self, text: str) -> str:
        match = re.search(EMAIL_PATTERN, text)
        return match.group(0) if match else ""
    
    def _extract_phone(self, text: str) -> str:
        match = re.search(PHONE_PATTERN, text)
        if match:
            phone = match.group(0)
            return phone.replace('+91', '').strip()
        return ""
    
    def _extract_name(self, text: str) -> str:
        lines = text.strip().split('\n')
        
        if lines:
            first_line = lines[0].strip()
            if len(first_line) < 50 and len(first_line.split()) <= 4:
                words = first_line.split()
                if all(w[0].isupper() if w else False for w in words if len(w) > 1):
                    if not any(c in first_line.lower() for c in ['email', 'phone', 'address', 'mobile', '@']):
                        return first_line
        
        for pattern in self.name_patterns:
            matches = re.findall(pattern, text[:500])
            for match in matches:
                if len(match) > 3 and len(match.split()) <= 4:
                    if not any(c in match.lower() for c in ['email', 'phone', 'address', 'www', 'http']):
                        return match.strip()
        
        return ""
    
    def _extract_location(self, text: str) -> str:
        text_lower = text.lower()
        
        for city in self.cities:
            if city in text_lower:
                return city.title()
        
        location_patterns = [
            r'(?:address|location|city|residing|located)[:\s]+([A-Za-z\s,]+)',
            r'(?:from|based in)[:\s]+([A-Za-z\s,]+)',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip().title()
        
        return ""
    
    def _extract_education(self, text: str) -> List[Education]:
        education = []
        lines = text.split('\n')
        
        edu_pattern = r'(?:university|college|institute|school|academy|institution)'
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            if any(keyword in line_lower for keyword in DEGREE_KEYWORDS):
                degree = self._extract_degree(line)
                
                institution = self._extract_institution(line, lines, i)
                
                year = self._extract_year(line)
                
                if degree or institution:
                    education.append(Education(
                        institution=institution or "",
                        degree=degree or "",
                        year=year or ""
                    ))
            
            elif re.search(edu_pattern, line_lower):
                institution = line.strip()
                year = self._extract_year(line)
                
                education.append(Education(
                    institution=institution,
                    degree="",
                    year=year or ""
                ))
        
        return education[:5]
    
    def _extract_degree(self, text: str) -> str:
        degree_mapping = {
            'b.tech': 'B.Tech',
            'b.e.': 'B.E.',
            'b.e ': 'B.E.',
            'b.sc': 'B.Sc',
            'b.com': 'B.Com',
            'b.a': 'B.A',
            'bba': 'BBA',
            'bca': 'BCA',
            'm.tech': 'M.Tech',
            'm.e.': 'M.E.',
            'm.sc': 'M.Sc',
            'm.com': 'M.Com',
            'mba': 'MBA',
            'mca': 'MCA',
            'ph.d': 'Ph.D',
            'phd': 'Ph.D',
        }
        
        text_lower = text.lower()
        for pattern, degree in degree_mapping.items():
            if pattern in text_lower:
                return degree
        
        for keyword in DEGREE_KEYWORDS:
            if keyword in text_lower:
                return keyword.upper()
        
        return ""
    
    def _extract_institution(self, line: str, lines: List[str], idx: int) -> str:
        institutions = [
            'iit', 'nit', 'iiit', 'bits', 'vit', 'amrita', 'manipal',
            'jntu', 'ou', 'osmania', 'deccan', 'gurunanak',
            'nawab', 'chancellor', 'university', 'college', 'institute',
            'rvce', 'jntuh', 'jntuk', 'iim', 'iisc'
        ]
        
        line_lower = line.lower()
        for inst in institutions:
            if inst in line_lower:
                return line.strip()
        
        if idx + 1 < len(lines):
            next_line = lines[idx + 1].lower()
            for inst in institutions:
                if inst in next_line:
                    return lines[idx + 1].strip()
        
        return ""
    
    def _extract_year(self, text: str) -> str:
        year_pattern = r'(?:19|20)\d{2}'
        match = re.search(year_pattern, text)
        if match:
            return match.group(0)
        
        year_range = r'(?:19|20)\d{2}\s*[-–]\s*(?:19|20)?\d{2}'
        match = re.search(year_range, text)
        if match:
            return match.group(0)
        
        return ""
    
    def _extract_experience(self, text: str) -> List[Experience]:
        experience = []
        lines = text.split('\n')
        
        exp_section = False
        exp_keywords = ['experience', 'employment', 'work history', 'professional background', 'career']
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            if any(kw in line_lower for kw in exp_keywords):
                exp_section = True
                continue
            
            if exp_section:
                if any(kw in line_lower for kw in ['education', 'skills', 'projects', 'certifications', 'academic']):
                    break
                
                if len(line.strip()) > 10:
                    company = self._extract_company(line, lines, i)
                    role = self._extract_role(line)
                    duration = self._extract_duration(line)
                    
                    if company or role:
                        experience.append(Experience(
                            company=company or "",
                            role=role or line.strip()[:50],
                            duration=duration or ""
                        ))
        
        if not experience:
            for line in lines:
                if re.search(r'\d+\s*(?:years?|months?)\s*(?:of)?\s*(?:experience|exp)', line.lower()):
                    exp = Experience(
                        company="",
                        role="Experience Detected",
                        duration=line.strip()
                    )
                    experience.append(exp)
                    break
        
        return experience[:5]
    
    def _extract_company(self, line: str, lines: List[str], idx: int) -> str:
        companies = [
            'tcs', 'infosys', 'wipro', 'accenture', 'cognizant', 'capgemini',
            'hcl', 'tech mahindra', 'amazon', 'google', 'microsoft', 'apple',
            'flipkart', 'paytm', 'ola', 'uber', 'swiggy', 'zomato',
            'facebook', 'meta', 'netflix', 'adobe', 'oracle', 'salesforce',
            'ibm', 'dell', 'hp', 'intel', 'amd', 'nvidia', 'qualcomm',
            'byju', 'unacademy', 'upgrad', 'swiggy', 'rapido', ' Dunzo'
        ]
        
        line_lower = line.lower()
        for company in companies:
            if company in line_lower:
                return company.title()
        
        for pattern in self.company_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_role(self, text: str) -> str:
        role_keywords = [
            'engineer', 'developer', 'manager', 'analyst', 'designer',
            'consultant', 'architect', 'lead', 'senior', 'junior',
            'intern', 'trainee', 'associate', 'specialist', 'coordinator',
            'executive', 'officer', 'supervisor', 'head', 'director', 'vp',
            'founder', 'co-founder', 'ceo', 'cto', 'cfo', 'product'
        ]
        
        text_lower = text.lower()
        for keyword in role_keywords:
            if keyword in text_lower:
                return text.strip()
        
        return ""
    
    def _extract_duration(self, text: str) -> str:
        duration_patterns = [
            r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[\s,]+\d{4}[\s,-]+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?[a-z]*[\s,]?\d{0,4}',
            r'(?:19|20)\d{2}\s*[-–]\s*(?:present|current|now|19|20)?\d{0,4}',
            r'\d+\s*(?:years?|months?)\s*(?:of)?\s*(?:experience|exp)',
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return ""
    
    def _extract_skills(self, text: str) -> List[str]:
        text_lower = text.lower()
        
        found_skills = set()
        
        words = re.findall(r'\b\w+\b', text_lower)
        
        for skill in ALL_SKILLS:
            if skill in text_lower:
                found_skills.add(skill)
            elif len(skill) > 3:
                for word in words:
                    if word.startswith(skill[:4]) and len(word) >= len(skill) - 2:
                        found_skills.add(skill)
        
        skill_list = sorted(list(found_skills))
        
        return skill_list[:50]


def extract_from_text(text: str) -> ExtractedData:
    extractor = NLPExtractor()
    return extractor.extract_all(text)
