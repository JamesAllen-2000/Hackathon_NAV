import easyocr
from PIL import Image
import os
from typing import List, Union
import numpy as np


class OCRHandler:
    """Handler for Optical Character Recognition using EasyOCR (no external dependencies)"""
    
    def __init__(self, languages: List[str] = None):
        """
        Initialize OCR handler
        
        Args:
            languages: List of language codes (default: ['en'] for English)
        """
        self.languages = languages or ['en']
        self.reader = None
        print(f"Initializing EasyOCR for languages: {self.languages}")
    
    def _load_reader(self):
        """Lazy load the EasyOCR reader"""
        if self.reader is None:
            print("Loading EasyOCR models (first run may take a moment)...")
            self.reader = easyocr.Reader(self.languages, gpu=False)
            print("✓ EasyOCR ready")
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from a single image
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Extracted text as string
        """
        try:
            
            self._load_reader()
            
           
            results = self.reader.readtext(image_path)
            
            
            text = ' '.join([detection[1] for detection in results])
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"OCR Error for {image_path}: {str(e)}")
    
    def extract_text_from_images(self, image_paths: List[str]) -> str:
        """
        Extract text from multiple images
        
        Args:
            image_paths: List of paths to image files
            
        Returns:
            Combined extracted text
        """
        all_text = []
        
        for i, path in enumerate(image_paths, 1):
            try:
                text = self.extract_text_from_image(path)
                if text:
                    all_text.append(f"--- Screen {i} ---\n{text}")
            except Exception as e:
                print(f"Warning: Failed to process {path}: {str(e)}")
                continue
        
        return "\n\n".join(all_text)
    
    def extract_text_from_pil_image(self, image: Image.Image) -> str:
        """
        Extract text from PIL Image object
        
        Args:
            image: PIL Image object
            
        Returns:
            Extracted text as string
        """
        try:
            
            self._load_reader()
            
            
            image_np = np.array(image)
            
           
            results = self.reader.readtext(image_np)
            
            
            text = ' '.join([detection[1] for detection in results])
            
            return text.strip()
        except Exception as e:
            raise Exception(f"OCR Error: {str(e)}")
