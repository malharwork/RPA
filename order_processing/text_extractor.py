import os
import logging
import PyPDF2
import pytesseract
from PIL import Image
import cv2
import numpy as np

class TextExtractor:
    """Extracts text from various file formats"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        self.ocr_language = self.config.get('processing.ocr_language', 'eng')
    
    def extract_from_file(self, file_path: str) -> str:
        """Extract text from various file formats"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            self.logger.info(f"Extracting text from: {file_path}")
            
            if file_extension == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp']:
                return self._extract_from_image(file_path)
            elif file_extension == '.txt':
                return self._extract_from_text(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
                
        except Exception as e:
            self.logger.error(f"Error extracting text from {file_path}: {str(e)}")
            raise
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    text += page_text
                    self.logger.debug(f"Extracted text from page {page_num + 1}")
        except Exception as e:
            self.logger.error(f"Error reading PDF {file_path}: {str(e)}")
            raise
        
        return text
    
    def _extract_from_image(self, file_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            # Load image
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError(f"Could not load image: {file_path}")
            
            # Preprocess image for better OCR
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to get better contrast
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(thresh, lang=self.ocr_language)
            
            self.logger.info(f"OCR completed for image: {file_path}")
            return text
            
        except Exception as e:
            self.logger.error(f"Error processing image {file_path}: {str(e)}")
            raise
    
    def _extract_from_text(self, file_path: str) -> str:
        """Extract text from plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            self.logger.info(f"Text extracted from: {file_path}")
            return text
        except Exception as e:
            self.logger.error(f"Error reading text file {file_path}: {str(e)}")
            raise