import re
from typing import Dict, Any, List
from utils.llm_client import LLMClient, PromptTemplates
from config import SCORING_CRITERIA


class EvaluationAgent:
    """
    Agent responsible for evaluating interview performance and providing feedback
    """
    
    def __init__(self):
        """Initialize Evaluation Agent"""
        self.llm_client = LLMClient()
    
    def evaluate(self, project_context: Dict[str, Any], qa_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Evaluate the interview performance
        
        Args:
            project_context: Dictionary with project information
            qa_history: List of Q&A dictionaries
            
        Returns:
            Dictionary containing scores and feedback
        """
        print("Evaluating interview performance...")
        
        prompt = PromptTemplates.evaluation_prompt(project_context, qa_history)
        
        try:
            
            response = self.llm_client.generate(prompt, max_tokens=700)
     
            evaluation = self._parse_evaluation_response(response)
            
            evaluation["final_score"] = self._calculate_final_score(evaluation)
            
            print("✓ Evaluation complete")
            return evaluation
            
        except Exception as e:
            print(f"✗ Evaluation Error: {str(e)}")
            return {
                "clarity": 5.0,
                "technical_depth": 5.0,
                "completeness": 5.0,
                "final_score": 5.0,
                "feedback": "Unable to complete evaluation due to technical error.",
                "raw_response": str(e)
            }
    
    def _parse_evaluation_response(self, response: str) -> Dict[str, Any]:
        """
        Parse evaluation response from LLM
        
        Args:
            response: Raw LLM response
            
        Returns:
            Dictionary with parsed scores and feedback
        """
        evaluation = {
            "clarity": 0.0,
            "technical_depth": 0.0,
            "completeness": 0.0,
            "feedback": "",
            "raw_response": response
        }
        
        clarity_match = re.search(r'CLARITY:\s*(\d+(?:\.\d+)?)', response, re.IGNORECASE)
        if clarity_match:
            evaluation["clarity"] = float(clarity_match.group(1))
        tech_match = re.search(r'TECHNICAL[_\s]DEPTH:\s*(\d+(?:\.\d+)?)', response, re.IGNORECASE)
        if tech_match:
            evaluation["technical_depth"] = float(tech_match.group(1))
        complete_match = re.search(r'COMPLETENESS:\s*(\d+(?:\.\d+)?)', response, re.IGNORECASE)
        if complete_match:
            evaluation["completeness"] = float(complete_match.group(1))
        feedback_match = re.search(r'FEEDBACK:\s*(.+?)$', response, re.DOTALL | re.IGNORECASE)
        if feedback_match:
            evaluation["feedback"] = feedback_match.group(1).strip()
        else:
            evaluation["feedback"] = response
        
        return evaluation
    
    def _calculate_final_score(self, evaluation: Dict[str, Any]) -> float:
        """
        Calculate weighted final score
        
        Args:
            evaluation: Dictionary with individual scores
            
        Returns:
            Weighted final score (0-10)
        """
        clarity = evaluation.get("clarity", 0.0)
        technical_depth = evaluation.get("technical_depth", 0.0)
        completeness = evaluation.get("completeness", 0.0)
        clarity_weight = SCORING_CRITERIA["clarity"]["weight"]
        tech_weight = SCORING_CRITERIA["technical_depth"]["weight"]
        complete_weight = SCORING_CRITERIA["completeness"]["weight"]
        final_score = (
            clarity * clarity_weight +
            technical_depth * tech_weight +
            completeness * complete_weight
        )
    
        final_score = max(0.0, min(10.0, final_score))
        
        return round(final_score, 2)
    
    def generate_score_interpretation(self, final_score: float) -> str:
        """
        Generate human-readable interpretation of the score
        
        Args:
            final_score: Final score (0-10)
            
        Returns:
            Interpretation string
        """
        if final_score >= 9.0:
            return "Outstanding - Exceptional understanding and communication"
        elif final_score >= 8.0:
            return "Excellent - Strong technical knowledge and clarity"
        elif final_score >= 7.0:
            return "Good - Solid understanding with minor gaps"
        elif final_score >= 6.0:
            return "Satisfactory - Adequate knowledge, room for improvement"
        elif final_score >= 5.0:
            return "Fair - Basic understanding, needs more depth"
        else:
            return "Needs Improvement - Significant gaps in understanding"
