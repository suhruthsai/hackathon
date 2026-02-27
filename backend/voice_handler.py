import io
import re
from typing import Optional
from modules.schemas import ExtractedData
from backend.nlp_extractor import extract_from_text


class VoiceHandler:
    def __init__(self):
        self.speech_recognition_available = False
        self.recognition = None
        
        try:
            import speech_recognition as sr
            self.recognition = sr.Recognizer()
            self.speech_recognition_available = True
            self.sr = sr
        except ImportError:
            pass
    
    def is_available(self) -> bool:
        return self.speech_recognition_available
    
    def speech_to_text_from_mic(self) -> str:
        if not self.speech_recognition_available:
            return ""
        
        try:
            with self.sr.Microphone() as source:
                self.recognition.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognition.listen(source, timeout=10)
            
            text = self.recognition.recognize_google(audio)
            return text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def speech_to_text_from_file(self, audio_file) -> str:
        if not self.speech_recognition_available:
            return ""
        
        try:
            audio_bytes = audio_file.getvalue()
            audio_data = io.BytesIO(audio_bytes)
            
            text = self.recognition.recognize_google(audio_data)
            return text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def process_voice_input(self, text: str) -> ExtractedData:
        return extract_from_text(text)


class VoiceInputSimulator:
    SAMPLE_VOICE_TEXTS = {
        "basic": "My name is Rahul Kumar. My email is rahul.kumar@example.com. My phone number is nine eight seven six five four three two one zero. I am from Hyderabad. I have done B.Tech in Computer Science from IIT Hyderabad. I have three years of experience in software development. My skills are Python, Java, React, SQL and Machine Learning.",
        
        "detailed": "Hello, I am Priya Sharma. You can reach me at priya.sharma@techmail.com or call me at nine one nine nine eight seven six five four three two. I live in Bangalore. I completed my B.E in Information Technology from RV College of Engineering in twenty nineteen and MBA from IIM Bangalore in twenty twenty one. I have five years of work experience including two years at TCS as software engineer and three years at Amazon as senior software developer. I am skilled in Python, Java, JavaScript, AWS, Docker and Kubernetes.",
        
        "minimal": "I am Amit Patel. Email amit@yahoo.com. Phone nine four four five six seven eight nine zero. B.Sc Chemistry from Mumbai University. One year internship."
    }
    
    @classmethod
    def get_sample_text(cls, level: str = "basic") -> str:
        return cls.SAMPLE_VOICE_TEXTS.get(level, cls.SAMPLE_VOICE_TEXTS["basic"])


def get_voice_handler() -> VoiceHandler:
    return VoiceHandler()


def process_voice_text(text: str) -> ExtractedData:
    return extract_from_text(text)
