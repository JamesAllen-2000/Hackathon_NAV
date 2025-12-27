import re
from typing import Dict, Any
from utils.llm_client import LLMClient, PromptTemplates


class UnderstandingAgent:
    """
    Agent responsible for understanding the project context from perception data
    """
    
    def __init__(self):
        """Initialize Understanding Agent"""
        self.llm_client = LLMClient()
    
    def understand(self, perception_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze perception data to understand the project
        
        Args:
            perception_data: Dictionary with screen_text and audio_transcript
            
        Returns:
            Dictionary containing project context (summary, tech_stack, complexity, features)
        """
        print("Analyzing project context...")
        
        # Generate prompt for understanding
        prompt = PromptTemplates.understanding_prompt(perception_data)
        
        try:
            # Get LLM response
            response = self.llm_client.generate(prompt, max_tokens=600)
            
            # Parse the response
            context = self._parse_understanding_response(response)
            
            print("✓ Project context analyzed")
            return context
            
        except Exception as e:
            print(f"✗ Understanding Error: {str(e)}")
            # Return default context on error
            return {
                "summary": "Unable to analyze project",
                "tech_stack": "Unknown",
                "complexity": "Unknown",
                "features": "N/A",
                "raw_response": str(e)
            }
    
    def _parse_understanding_response(self, response: str) -> Dict[str, Any]:
        """
        Parse LLM response to extract structured project context
        
        Args:
            response: Raw LLM response text
            
        Returns:
            Structured dictionary with project information
        """
        context = {
            "summary": "",
            "tech_stack": "",
            "complexity": "",
            "features": "",
            "raw_response": response
        }
        
        # Try to extract structured fields
        summary_match = re.search(r'SUMMARY:\s*(.+?)(?=\n(?:TECH_STACK|COMPLEXITY|FEATURES)|$)', response, re.DOTALL | re.IGNORECASE)
        if summary_match:
            context["summary"] = summary_match.group(1).strip()
        
        tech_match = re.search(r'TECH_STACK:\s*(.+?)(?=\n(?:SUMMARY|COMPLEXITY|FEATURES)|$)', response, re.DOTALL | re.IGNORECASE)
        if tech_match:
            context["tech_stack"] = tech_match.group(1).strip()
        
        complexity_match = re.search(r'COMPLEXITY:\s*(.+?)(?=\n(?:SUMMARY|TECH_STACK|FEATURES)|$)', response, re.DOTALL | re.IGNORECASE)
        if complexity_match:
            context["complexity"] = complexity_match.group(1).strip()
        
        features_match = re.search(r'FEATURES:\s*(.+?)(?=\n(?:SUMMARY|TECH_STACK|COMPLEXITY)|$)', response, re.DOTALL | re.IGNORECASE)
        if features_match:
            context["features"] = features_match.group(1).strip()
        
        # Fallback: if structured parsing failed, use the whole response as summary
        if not context["summary"] and response:
            context["summary"] = response[:500]  # Take first 500 chars
        
        return context
