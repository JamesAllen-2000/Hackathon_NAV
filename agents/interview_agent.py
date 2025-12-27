import re
from typing import Dict, Any, List
from utils.llm_client import LLMClient, PromptTemplates
from config import NUM_INITIAL_QUESTIONS, NUM_FOLLOWUP_QUESTIONS


class InterviewAgent:
    """
    Agent responsible for conducting the interview with context-aware questions
    """
    
    def __init__(self):
        """Initialize Interview Agent"""
        self.llm_client = LLMClient()
        self.qa_history = []
    
    def generate_initial_questions(self, project_context: Dict[str, Any]) -> List[str]:
        """
        Generate initial interview questions based on project context
        
        Args:
            project_context: Dictionary with project information
            
        Returns:
            List of interview questions
        """
        print(f"Generating {NUM_INITIAL_QUESTIONS} initial interview questions...")
        
        
        prompt = PromptTemplates.interview_prompt(project_context)
        
        try:
            
            response = self.llm_client.generate(prompt, max_tokens=400)
            
            
            questions = self._parse_questions(response)
            
            
            if not questions or len(questions) < NUM_INITIAL_QUESTIONS:
                questions = self._extract_questions_fallback(response)
            
            print(f"✓ Generated {len(questions)} questions")
            return questions[:NUM_INITIAL_QUESTIONS]
            
        except Exception as e:
            print(f"✗ Question Generation Error: {str(e)}")
        
            return [
                "Can you explain the main purpose of your project?",
                "What technologies did you use and why?",
                "What challenges did you face during development?"
            ]
    
    def generate_followup_question(self, question: str, answer: str, project_context: Dict[str, Any]) -> str:
        """
        Generate adaptive follow-up question based on student's answer
        
        Args:
            question: Original question
            answer: Student's answer
            project_context: Project context dictionary
            
        Returns:
            Follow-up question string
        """
        print("Generating follow-up question...")
        
      
        prompt = PromptTemplates.followup_prompt(question, answer, project_context)
        
        try:

            response = self.llm_client.generate(prompt, max_tokens=200)
            
           
            followup = self._parse_followup(response)
            
            print("✓ Follow-up question generated")
            return followup
            
        except Exception as e:
            print(f"✗ Follow-up Generation Error: {str(e)}")
            return "Can you elaborate more on that?"
    
    def add_qa_to_history(self, question: str, answer: str):
        """
        Add Q&A pair to interview history
        
        Args:
            question: Question asked
            answer: Student's answer
        """
        self.qa_history.append({
            "question": question,
            "answer": answer
        })
    
    def get_qa_history(self) -> List[Dict[str, str]]:
        """Get the complete Q&A history"""
        return self.qa_history
    
    def _parse_questions(self, response: str) -> List[str]:
        """
        Parse questions from LLM response
        
        Args:
            response: Raw LLM response
            
        Returns:
            List of parsed questions
        """
        questions = []
        
        
        pattern = r'Q\d+:\s*(.+?)(?=\n(?:Q\d+:|$))'
        matches = re.findall(pattern, response, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            question = match.strip()
            if question and len(question) > 10:  
                questions.append(question)
        
        return questions
    
    def _extract_questions_fallback(self, response: str) -> List[str]:
        """
        Fallback method to extract questions from response
        
        Args:
            response: Raw LLM response
            
        Returns:
            List of extracted questions
        """
        questions = []
        
        
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            
            line = re.sub(r'^[\d\.\-\*\)]+\s*', '', line)
            
            if '?' in line and len(line) > 20:
                questions.append(line)
        
        return questions
    
    def _parse_followup(self, response: str) -> str:
        """
        Parse follow-up question from LLM response
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed follow-up question
        """
        
        followup_match = re.search(r'FOLLOWUP:\s*(.+?)$', response, re.DOTALL | re.IGNORECASE)
        if followup_match:
            return followup_match.group(1).strip()
        
        
        lines = response.split('\n')
        for line in lines:
            if '?' in line:
                return line.strip()
        
        
        return response.strip()
