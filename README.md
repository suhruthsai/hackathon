# DEET Smart Registration System

AI-powered resume parser for Digital Employment Exchange of Telangana (DEET).

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**Note:** For PDF processing, you'll also need Poppler:
- Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases/
- Mac: `brew install poppler`
- Linux: `sudo apt-get install poppler-utils`

**For Tesseract OCR:**
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- Mac: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

### 2. Run the Application

```bash
streamlit run app.py
```

## Features

- **Resume Upload**: Support for PDF, JPG, PNG formats
- **OCR Processing**: Tesseract-based text extraction with image preprocessing
- **NLP Extraction**: spaCy-powered entity extraction (name, email, phone, skills, education, experience)
- **Fraud Detection**: Validates phone, email, checks for suspicious keywords
- **Health Score**: Calculates resume completeness (0-100)
- **Editable Preview**: All extracted fields can be corrected
- **Voice Input**: Optional voice-based registration with sample texts
- **DEET Submission**: Generates JSON payload matching DEET API schema
- **Accuracy Evaluation**: Built-in test suite with 10 sample resumes

## Project Structure

```
DEET-Smart-Registration/
├── app.py                      # Main Streamlit application
├── backend/
│   ├── ocr_engine.py           # PDF/image to text conversion
│   ├── nlp_extractor.py        # spaCy + regex extraction
│   ├── fraud_detector.py       # Fraud detection logic
│   ├── health_scorer.py       # Resume health scoring
│   ├── voice_handler.py       # Voice input processing
│   └── submission_sim.py       # DEET API simulation
├── modules/
│   ├── config.py               # Skills list, patterns, configuration
│   ├── schemas.py              # Data models
│   └── evaluation.py           # Accuracy testing module
├── SPEC.md                     # Detailed specification
└── requirements.txt            # Python dependencies
```

## Usage Flow

1. **Upload**: Drop a resume (PDF/JPG/PNG) or use voice input
2. **Review**: Edit extracted information in the Preview tab
3. **Analyze**: View health score and fraud detection report
4. **Submit**: Generate and submit DEET-compatible JSON payload

## Evaluation

Navigate to the "Evaluate" tab to run accuracy tests on sample resumes.

## Tech Stack

- **Frontend**: Streamlit
- **OCR**: pytesseract, pdf2image, Pillow
- **NLP**: spaCy (en_core_web_sm)
- **Speech**: SpeechRecognition (optional)
- **Data**: Python dataclasses

## Hackathon Demo Script

1. **Opening** (30s): Explain DEET problem and solution
2. **Live Demo** (3min):
   - Upload sample resume
   - Show OCR processing
   - Review editable form
   - Display fraud detection
   - Show health score
   - Submit to DEET
3. **Voice Mode** (1min): Demonstrate voice input
4. **Evaluation** (30s): Run accuracy tests
5. **Closing** (30s): Recap differentiators

## Notes

- OCR accuracy depends on image quality
- Always verify extracted data before submission
- Voice mode requires microphone permission
- For production: integrate with actual DEET API
