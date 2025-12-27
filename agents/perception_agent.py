from typing import List, Dict, Any
from utils.ocr_handler import OCRHandler


class PerceptionAgent:
    """
    Agent responsible for perceiving the presentation via OCR
    Audio transcription is handled by browser Web Speech API
    """
    
    def __init__(self, ocr_languages: list = None):
        """
        Initialize Perception Agent
        
        Args:
            ocr_languages: List of language codes for OCR (default: ['en'])
        """
        self.ocr_handler = OCRHandler(languages=ocr_languages)
    
    def perceive(self, image_paths: List[str] = None, audio_paths: List[str] = None) -> Dict[str, Any]:
        """
        Process presentation inputs through OCR and STT
        
        Args:
            image_paths: List of screenshot/image file paths
            audio_paths: List of audio file paths
            
        Returns:
            Dictionary containing screen_text and audio_transcript
        """
        perception_data = {
            "screen_text": "",
            "audio_transcript": ""
        }
        
       
        if image_paths:
            print("Processing screenshots with OCR...")
            try:
                perception_data["screen_text"] = self.ocr_handler.extract_text_from_images(image_paths)
                print(f"✓ Extracted text from {len(image_paths)} image(s)")
            except Exception as e:
                print(f"✗ OCR Error: {str(e)}")
                perception_data["screen_text"] = "[OCR processing failed]"
        
        
        return perception_data
    
    def perceive_single(self, image_path: str = None, audio_path: str = None) -> Dict[str, Any]:
        """
        Process single image and audio file
        
        Args:
            image_path: Path to screenshot/image file
            audio_path: Path to audio file
            
        Returns:
            Dictionary containing screen_text and audio_transcript
        """
        image_paths = [image_path] if image_path else None
        audio_paths = [audio_path] if audio_path else None
        
        return self.perceive(image_paths, audio_paths)
