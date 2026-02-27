import io
import re
from typing import Optional
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

try:
    from pdf2image import convert_from_bytes
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False


class OCREngine:
    def __init__(self):
        self.supported_formats = ['pdf', 'jpg', 'jpeg', 'png']
    
    def process_file(self, file_bytes: bytes, filename: str) -> str:
        ext = filename.split('.')[-1].lower()
        
        if ext == 'pdf':
            return self._process_pdf(file_bytes)
        elif ext in ['jpg', 'jpeg', 'png']:
            return self._process_image(file_bytes)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    def _process_pdf(self, file_bytes: bytes) -> str:
        if not PDF2IMAGE_AVAILABLE:
            raise ImportError("pdf2image not available. Please install poppler-utils.")
        
        images = convert_from_bytes(file_bytes)
        full_text = ""
        
        for i, image in enumerate(images):
            text = self._extract_text_from_image(image)
            full_text += f"\n--- Page {i+1} ---\n{text}"
        
        return self._cleanup_text(full_text)
    
    def _process_image(self, file_bytes: bytes) -> str:
        image = Image.open(io.BytesIO(file_bytes))
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        text = self._extract_text_from_image(image)
        return self._cleanup_text(text)
    
    def _extract_text_from_image(self, image: Image.Image) -> str:
        gray = image.convert('L')
        
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(1.5)
        
        enhanced = enhanced.filter(ImageFilter.MedianFilter(size=3))
        
        text = pytesseract.image_to_string(
            enhanced,
            config='--psm 6 --oem 3'
        )
        
        return text
    
    def _cleanup_text(self, text: str) -> str:
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        
        text = re.sub(r'\s+', ' ', text)
        
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        text = '\n'.join(cleaned_lines)
        
        return text


def extract_text_from_file(uploaded_file) -> str:
    engine = OCREngine()
    file_bytes = uploaded_file.getvalue()
    filename = uploaded_file.name
    return engine.process_file(file_bytes, filename)
