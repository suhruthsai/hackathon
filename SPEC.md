# DEET Smart Registration System - Specification

## 1. Project Overview

**Project Name:** DEET Smart Registration System  
**Type:** Full-stack AI-powered web application  
**Core Functionality:** AI-powered resume parser that extracts structured data from uploaded resumes, validates for fraud, calculates health scores, and generates DEET-ready JSON payloads  
**Target Users:** Job seekers in Telangana, employment exchange staff, hackathon evaluators

---

## 2. Technical Architecture

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Streamlit)                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐  │
│  │Upload Zone  │ │ Edit Form   │ │ Voice Mode  │ │ Dashboard │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (Python/Flask)                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐  │
│  │File Handler │ │ OCR Engine  │ │ NLP Pipeline│ │  Validator│  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      NLP & AI LAYER                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐  │
│  │pdf2image    │ │pytesseract │ │spaCy        │ │  Regex    │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Frontend | Streamlit | 1.28+ |
| Backend | Python | 3.10+ |
| OCR | pytesseract + pdf2image | latest |
| NLP | spaCy | 3.7+ |
| Speech | SpeechRecognition + pydub | latest |
| PDF Handling | PyPDF2, pdf2image | latest |
| Image Processing | Pillow, OpenCV | latest |

### 2.3 Folder Structure

```
DEET-Smart-Registration/
├── app.py                      # Main Streamlit app
├── backend/
│   ├── __init__.py
│   ├── ocr_engine.py           # PDF/image to text
│   ├── nlp_extractor.py        # spaCy + regex extraction
│   ├── fraud_detector.py      # Fraud detection logic
│   ├── health_scorer.py       # Resume health scoring
│   ├── voice_handler.py       # Voice input processing
│   └── submission_sim.py      # DEET API simulation
├── modules/
│   ├── __init__.py
│   ├── config.py              # Skills list, patterns
│   ├── schemas.py             # Data models
│   └── evaluation.py          # Accuracy testing
├── sample_resumes/            # Test resumes
├── requirements.txt
└── README.md
```

---

## 3. Functional Specifications

### 3.1 Resume Upload Module

**Supported Formats:** PDF, JPG, PNG

**Processing Flow:**
1. Accept file via drag-drop or file picker
2. Validate file type and size (<10MB)
3. If PDF: Convert pages to images using pdf2image
4. Pass images to Tesseract OCR
5. Extract raw text with basic cleanup

**Error Handling:**
- Malformed PDF → Show error with manual entry fallback
- OCR failure → Allow direct text input

### 3.2 OCR Processing

```python
def process_image(image):
    # Convert to grayscale
    # Apply thresholding
    # Extract text with pytesseract
    # Basic cleanup: remove extra whitespace, fix common OCR errors
    return cleaned_text
```

### 3.3 Structured Extraction Pipeline

#### A. Regex Extraction
| Field | Pattern |
|-------|---------|
| Email | `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` |
| Phone | `(\+91)?[6-9]\d{9}` |
| URL | `https?://[^\s]+` |

#### B. spaCy NLP Extraction
| Entity | Mapping |
|--------|---------|
| PERSON | candidate_name |
| ORG | education, companies |
| GPE | location |
| DATE | experience timeline |

**Filtering Rules:**
- Remove entities with length < 2
- Remove common stop words incorrectly tagged as ORG
- Deduplicate extracted entities

#### C. Skills Extraction
- Tokenize resume text
- Match against predefined skills list (500+ skills)
- Case insensitive matching
- Categories: Programming, Tools, Frameworks, Soft Skills

### 3.4 Fraud Detection Layer

**Fraud Checks:**
| Check | Condition | Weight |
|-------|-----------|--------|
| Invalid Phone | Not 10 digits / invalid format | 20 |
| Invalid Email | Regex pattern fail | 15 |
| Experience-Age Mismatch | Experience > Age - 18 | 25 |
| Excessive Skills | > 50 skills detected | 15 |
| Suspicious Keywords | Contains "guarantee", "pay fee", "job without interview" | 25 |

**Output:**
```python
{
    "fraud_risk_score": 0-100,
    "risk_label": "Low" | "Moderate" | "High",
    "flags": [
        {"check": "phone_invalid", "severity": "high", "message": "..."}
    ]
}
```

### 3.5 Resume Health Score

**Scoring Criteria:**
| Component | Max Points | Condition |
|-----------|------------|-----------|
| Email | 10 | Present |
| Phone | 10 | Present |
| Education | 20 | At least 1 degree detected |
| Experience | 20 | At least 1 job detected |
| Skills | 20 | ≥ 5 skills |
| Address | 20 | Location detected |

**Display:**
- Progress bar (0-100)
- Color coding: Red (<50), Yellow (50-79), Green (≥80)
- Improvement suggestions list

### 3.6 Editable Preview Form

All extracted fields displayed as editable Streamlit form fields:
- Full Name (text input)
- Email (email input)
- Phone (text input)
- Location (text input)
- Education (dynamic list - add/remove)
- Experience (dynamic list - add/remove)
- Skills (multiselect/tag input)
- Raw Text (textarea, read-only with copy button)

### 3.7 DEET Form Integration

**JSON Payload Schema:**
```json
{
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
```

**Simulation:** Mock API call with success/failure response

### 3.8 Voice Registration (Optional)

**Flow:**
1. User clicks "Enable Voice Input"
2. Browser requests microphone permission
3. SpeechRecognition captures audio
4. Convert speech to text
5. Pass through NLP extraction pipeline
6. Auto-fill form fields

**Fallback:**
- "Upload audio file" option
- Pre-recorded sample audio

---

## 4. UI/UX Specifications

### 4.1 Layout Structure

**Single Page Application with Tabs:**
1. **Upload** - File drop zone, process button
2. **Preview** - Editable form with extracted data
3. **Analysis** - Health score, fraud report
4. **Submit** - JSON preview, submit button
5. **Evaluate** - Accuracy testing (admin mode)

### 4.2 Visual Design

**Color Palette:**
- Primary: #1E3A5F (Deep Navy)
- Secondary: #3498DB (Bright Blue)
- Accent: #2ECC71 (Success Green)
- Warning: #F39C12 (Orange)
- Danger: #E74C3C (Red)
- Background: #F8F9FA (Light Gray)
- Card: #FFFFFF (White)

**Typography:**
- Headings: Inter Bold, 24px/20px/18px
- Body: Inter Regular, 16px
- Labels: Inter Medium, 14px

**Spacing:**
- Section padding: 24px
- Card padding: 20px
- Element gap: 16px

### 4.3 Component States

**Buttons:**
- Default: Primary color, rounded corners (8px)
- Hover: 10% darker, slight elevation
- Active: 15% darker
- Disabled: 50% opacity

**Input Fields:**
- Default: 1px border #DDD
- Focus: 2px border Primary color
- Error: 2px border Danger color

---

## 5. Evaluation Module

### 5.1 Test Dataset

10 sample resumes with known ground truth:
- 3 PDF resumes (varied quality)
- 4 JPG resumes (scanned)
- 3 PNG resumes (photo of resume)

### 5.2 Evaluation Metrics

| Field | Metric |
|-------|--------|
| Email | Exact match |
| Phone | Exact match |
| Name | Partial match allowed (80%) |
| Skills | Intersection over Union |
| Education | Fuzzy match (Levenshtein) |

### 5.3 Results Table

```
| Resume | Field      | Expected    | Extracted   | Correct |
|--------|------------|-------------|-------------|---------|
| 1      | Email      | abc@xyz.com | abc@xyz.com | ✓       |
| 1      | Phone      | 9876543210  | 9876543210  | ✓       |
... (10 resumes × 7 fields)
```

**Summary:**
- Overall Accuracy: XX%
- Field-wise Accuracy Matrix

---

## 6. Non-Functional Requirements

### 6.1 Performance
- Extraction pipeline: < 10 seconds
- UI response: < 500ms
- spaCy model loaded once at startup (cached)

### 6.2 Reliability
- Graceful degradation for malformed PDFs
- Manual text input fallback always available
- Session state management for data persistence

### 6.3 Scalability
- Modular pipeline architecture
- Extensible fraud rules via configuration
- Ready for future DEET API integration

---

## 7. Demo Script (Hackathon)

### 7.1 Opening (30 seconds)
- Introduce DEET problem context
- Show current manual process pain points

### 7.2 Live Demo (3 minutes)
1. Upload sample resume (PDF)
2. Show OCR processing
3. Display extracted data in editable form
4. Show fraud detection alert (if applicable)
5. Demonstrate health score
6. Submit to DEET simulation

### 7.3 Voice Mode (1 minute)
1. Click voice button
2. Speak: "My name is..."
3. Auto-fill demonstration

### 7.4 Evaluation (30 seconds)
- Run accuracy test
- Show results table

### 7.5 Closing (30 seconds)
- Key differentiators recap
- Future roadmap

---

## 8. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| OCR failures | Manual text entry fallback |
| spaCy model missing | Auto-download with progress |
| Large PDF files | Size limit + progress indicator |
| Voice recognition fail | Text input fallback |
| Network issues | Fully offline-capable core |
