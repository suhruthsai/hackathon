import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime

st.set_page_config(
    page_title="DEET Smart Registration System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

from modules.schemas import ExtractedData, Education, Experience
from backend.ocr_engine import extract_text_from_file
from backend.nlp_extractor import extract_from_text
from backend.fraud_detector import detect_fraud
from backend.health_scorer import calculate_health_score
from backend.submission_sim import submit_to_deet, generate_deet_payload
from backend.voice_handler import VoiceInputSimulator, get_voice_handler
from modules.evaluation import run_evaluation, get_evaluation_results

COLORS = {
    "primary": "#1E3A5F",
    "secondary": "#3498DB",
    "accent": "#2ECC71",
    "warning": "#F39C12",
    "danger": "#E74C3C",
    "bg": "#F8F9FA",
    "card": "#FFFFFF"
}

st.markdown("""
<style>
    .main { background-color: #F8F9FA; }
    .stButton>button {
        background-color: #1E3A5F;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
    }
    .stButton>button:hover { background-color: #2C5282; }
    .css-1aumxhk { background-color: #1E3A5F; }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 16px;
    }
    .score-card {
        background: linear-gradient(135deg, #1E3A5F 0%, #3498DB 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
    }
    .fraud-high { border-left: 4px solid #E74C3C; }
    .fraud-moderate { border-left: 4px solid #F39C12; }
    .fraud-low { border-left: 4px solid #2ECC71; }
    .metric-value { font-size: 28px; font-weight: bold; }
    .metric-label { font-size: 14px; opacity: 0.8; }
    h1, h2, h3 { color: #1E3A5F; }
    .stTabs [data-baseweb="tab-list"] button { font-weight: 600; }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    if 'extracted_data' not in st.session_state:
        st.session_state.extracted_data = None
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'submission_result' not in st.session_state:
        st.session_state.submission_result = None
    if 'health_score' not in st.session_state:
        st.session_state.health_score = None
    if 'fraud_report' not in st.session_state:
        st.session_state.fraud_report = None
    if 'raw_text' not in st.session_state:
        st.session_state.raw_text = ""


def header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("")
        st.markdown("### DEET Smart Registration System")
        st.markdown("*AI-Powered Resume Parser for Digital Employment Exchange of Telangana*")
    with col2:
        st.markdown("")
        st.markdown(f"**Session:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")


def upload_section():
    st.markdown("### 1. Upload Resume")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Drop your resume here (PDF, JPG, PNG)",
            type=['pdf', 'jpg', 'jpeg', 'png'],
            help="Supported formats: PDF, JPG, PNG"
        )
    
    with col2:
        st.markdown("##### Or use voice input")
        voice_enabled = st.checkbox("Enable Voice Mode", value=False)
        
        if voice_enabled:
            voice_text = st.text_area("Enter voice transcription or use sample:", 
                                     height=100,
                                     placeholder="Or paste transcribed text here...")
            
            sample_level = st.selectbox("Load sample voice text:", 
                                        ["basic", "detailed", "minimal"])
            
            if st.button("Load Sample"):
                sample_text = VoiceInputSimulator.get_sample_text(sample_level)
                st.session_state.raw_text = sample_text
                st.session_state.extracted_data = extract_from_text(sample_text)
                st.session_state.processed = True
                st.success("Voice input processed!")
                st.rerun()
    
    if uploaded_file is not None:
        if st.button("Process Resume", type="primary"):
            with st.spinner("Extracting text from resume..."):
                try:
                    raw_text = extract_text_from_file(uploaded_file)
                    st.session_state.raw_text = raw_text
                    
                    with st.spinner("Analyzing resume with AI..."):
                        extracted = extract_from_text(raw_text)
                        st.session_state.extracted_data = extracted
                        
                        health = calculate_health_score(
                            extracted.email,
                            extracted.phone,
                            len(extracted.education),
                            len(extracted.experience),
                            extracted.skills,
                            extracted.location
                        )
                        st.session_state.health_score = health
                        
                        fraud = detect_fraud(
                            extracted.phone,
                            extracted.email,
                            extracted.skills,
                            len(extracted.experience),
                            raw_text
                        )
                        st.session_state.fraud_report = fraud
                        
                        st.session_state.processed = True
                    st.success("Resume processed successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error processing resume: {str(e)}")
                    st.info("Try using manual text input below")
    
    with st.expander("Manual Text Input (Fallback)"):
        manual_text = st.text_area("Paste resume text here:", height=150)
        if st.button("Process Text Input"):
            if manual_text:
                st.session_state.raw_text = manual_text
                extracted = extract_from_text(manual_text)
                st.session_state.extracted_data = extracted
                
                health = calculate_health_score(
                    extracted.email,
                    extracted.phone,
                    len(extracted.education),
                    len(extracted.experience),
                    extracted.skills,
                    extracted.location
                )
                st.session_state.health_score = health
                
                fraud = detect_fraud(
                    extracted.phone,
                    extracted.email,
                    extracted.skills,
                    len(extracted.experience),
                    manual_text
                )
                st.session_state.fraud_report = fraud
                
                st.session_state.processed = True
                st.success("Text processed successfully!")
                st.rerun()


def preview_section():
    st.markdown("### 2. Review & Edit Information")
    
    if not st.session_state.extracted_data:
        st.warning("No data to display. Please upload a resume first.")
        return
    
    data = st.session_state.extracted_data
    
    col1, col2 = st.columns(2)
    
    with col1:
        data.full_name = st.text_input("Full Name", value=data.full_name or "")
        data.email = st.text_input("Email", value=data.email or "")
        data.phone = st.text_input("Phone", value=data.phone or "")
    
    with col2:
        data.location = st.text_input("Location", value=data.location or "")
    
    st.markdown("#### Education")
    if not data.education:
        data.education = [Education(institution="", degree="", year="")]
    
    for i, edu in enumerate(data.education):
        with st.expander(f"Education {i+1}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                edu.institution = st.text_input(f"Institution {i+1}", value=edu.institution, key=f"edu_inst_{i}")
            with col2:
                edu.degree = st.text_input(f"Degree {i+1}", value=edu.degree, key=f"edu_deg_{i}")
            with col3:
                edu.year = st.text_input(f"Year {i+1}", value=edu.year, key=f"edu_yr_{i}")
    
    st.markdown("#### Experience")
    if not data.experience:
        data.experience = [Experience(company="", role="", duration="")]
    
    for i, exp in enumerate(data.experience):
        with st.expander(f"Experience {i+1}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                exp.company = st.text_input(f"Company {i+1}", value=exp.company, key=f"exp_comp_{i}")
            with col2:
                exp.role = st.text_input(f"Role {i+1}", value=exp.role, key=f"exp_role_{i}")
            with col3:
                exp.duration = st.text_input(f"Duration {i+1}", value=exp.duration, key=f"exp_dur_{i}")
    
    st.markdown("#### Skills")
    skills_text = st.text_area("Skills (comma-separated)", 
                                value=", ".join(data.skills),
                                help="Enter skills separated by commas")
    data.skills = [s.strip() for s in skills_text.split(",") if s.strip()]
    
    st.session_state.extracted_data = data
    
    st.markdown("#### Raw Extracted Text")
    st.text_area("Raw Text (Read-only)", 
                 value=st.session_state.raw_text[:2000] + "..." if len(st.session_state.raw_text) > 2000 else st.session_state.raw_text,
                 height=150,
                 disabled=True)


def analysis_section():
    st.markdown("### 3. Analysis & Validation")
    
    if not st.session_state.health_score:
        st.warning("No analysis available. Please process a resume first.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Resume Health Score")
        
        health = st.session_state.health_score
        
        score_color = "green" if health.total_score >= 80 else "orange" if health.total_score >= 50 else "red"
        
        st.markdown(f"""
        <div class="score-card">
            <div class="metric-value">{health.total_score}/100</div>
            <div class="metric-label">Health Score</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(health.total_score / 100)
        
        st.markdown("**Completeness Checklist:**")
        st.write(f"- Email: {'✓' if health.email_present else '✗'}")
        st.write(f"- Phone: {'✓' if health.phone_present else '✗'}")
        st.write(f"- Education: {'✓' if health.education_detected else '✗'}")
        st.write(f"- Experience: {'✓' if health.experience_detected else '✗'}")
        st.write(f"- Skills (≥5): {'✓' if health.skills_count >= 5 else '✗'}")
        st.write(f"- Location: {'✓' if health.address_detected else '✗'}")
        
        if health.suggestions:
            st.markdown("**Suggestions to Improve:**")
            for suggestion in health.suggestions:
                st.write(f"• {suggestion}")
    
    with col2:
        st.markdown("#### Fraud Detection Report")
        
        fraud = st.session_state.fraud_report
        
        fraud_class = f"fraud-{fraud.risk_label.lower()}"
        
        st.markdown(f"""
        <div class="card {fraud_class}">
            <h3 style="margin: 0;">Risk Level: {fraud.risk_label}</h3>
            <p class="metric-value">{fraud.fraud_risk_score}/100</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(fraud.fraud_risk_score / 100)
        
        if fraud.flags:
            st.markdown("**Risk Flags:**")
            for flag in fraud.flags:
                severity_icon = "🔴" if flag.severity == "high" else "🟡"
                st.write(f"{severity_icon} {flag.message}")
        else:
            st.success("No fraud indicators detected ✓")


def submission_section():
    st.markdown("### 4. Submit to DEET")
    
    if not st.session_state.extracted_data:
        st.warning("No data to submit. Please process a resume first.")
        return
    
    payload = generate_deet_payload(st.session_state.extracted_data)
    
    st.markdown("#### DEET API Payload")
    st.json(payload)
    
    with st.expander("View DEET API Schema"):
        st.code(json.dumps({
            "full_name": "string (required)",
            "email": "string (required)",
            "phone": "string (required)",
            "location": "string (optional)",
            "education": [{"institution": "string", "degree": "string", "year": "string"}],
            "experience": [{"company": "string", "role": "string", "duration": "string"}],
            "skills": ["string"]
        }, indent=2))
    
    if st.button("Submit Registration", type="primary"):
        with st.spinner("Submitting to DEET..."):
            result = submit_to_deet(st.session_state.extracted_data)
            st.session_state.submission_result = result
            st.session_state.submitted = True
        
        if result.success:
            st.success(f"✓ {result.message}")
            st.markdown(f"**Submission ID:** `{result.submission_id}`")
            st.markdown(f"**Timestamp:** {result.timestamp}")
        else:
            st.error(f"✗ {result.message}")


def evaluation_section():
    st.markdown("### 5. Accuracy Evaluation")
    st.markdown("*Test the NLP extraction accuracy on sample resumes*")
    
    if st.button("Run Evaluation"):
        with st.spinner("Evaluating extraction accuracy..."):
            results, report = get_evaluation_results()
        
        st.markdown(f"### Overall Accuracy: {report.accuracy_percentage:.1f}%")
        
        st.progress(report.accuracy_percentage / 100)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Fields", report.total_fields)
        with col2:
            st.metric("Correct", report.correct_fields)
        with col3:
            st.metric("Accuracy", f"{report.accuracy_percentage:.1f}%")
        
        st.markdown("#### Field-wise Accuracy")
        field_df = pd.DataFrame([
            {"Field": field, "Accuracy": f"{acc:.1f}%"}
            for field, acc in report.field_wise_accuracy.items()
        ])
        st.table(field_df)
        
        st.markdown("#### Detailed Results")
        
        results_data = []
        for r in results:
            results_data.append({
                "Resume": r.resume_name,
                "Field": r.field_name,
                "Expected": r.expected[:30] + "..." if len(r.expected) > 30 else r.expected,
                "Extracted": r.extracted[:30] + "..." if len(r.extracted) > 30 else r.extracted,
                "Correct": "✓" if r.correct else "✗"
            })
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True)


def main():
    init_session_state()
    
    header()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📤 Upload", "✏️ Preview", "📊 Analysis", "📤 Submit", "🧪 Evaluate"
    ])
    
    with tab1:
        upload_section()
    
    with tab2:
        preview_section()
    
    with tab3:
        analysis_section()
    
    with tab4:
        submission_section()
    
    with tab5:
        evaluation_section()
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>DEET Smart Registration System | AI-Powered Job Seeker Registration</p>
        <p>Built with Streamlit, spaCy, and Tesseract OCR</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
