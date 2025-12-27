import requests
import time
from typing import Dict, Any
from config import LLM_API_TOKEN, LLM_API_URL, LLM_MODEL_NAME, LLM_TEMPERATURE, LLM_MAX_TOKENS


class LLMClient:
    """Wrapper for LLM API (Groq or OpenAI-compatible)"""
    
    def __init__(self):
        self.api_url = LLM_API_URL
        self.headers = {
            "Authorization": f"Bearer {LLM_API_TOKEN}",
            "Content-Type": "application/json"
        }
    
    def generate(self, prompt: str, temperature: float = None, max_tokens: int = None) -> str:
        """
        Generate text response from LLM using OpenAI-compatible chat format
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (default from config)
            max_tokens: Maximum tokens to generate (default from config)
            
        Returns:
            Generated text response
        """
        temperature = temperature or LLM_TEMPERATURE
        max_tokens = max_tokens or LLM_MAX_TOKENS
        
        
        payload = {
            "model": LLM_MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
            
           
            return str(result)
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 503:
                
                print("Model is loading... waiting 20 seconds...")
                time.sleep(20)
                return self.generate(prompt, temperature, max_tokens)
            else:
                raise Exception(f"API Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"LLM Generation Error: {str(e)}")


class PromptTemplates:
    """Prompt templates for different agents"""
    
    @staticmethod
    def understanding_prompt(perception_data: Dict[str, Any]) -> str:
        """Generate prompt for understanding agent"""
        screen_text = perception_data.get("screen_text", "")
        audio_transcript = perception_data.get("audio_transcript", "")
        
        prompt = f"""Analyze the following project presentation data and extract key information.

Screen Content:
{screen_text}

Audio Transcript:
{audio_transcript}

Please provide:
1. Project Summary (2-3 sentences)
2. Technology Stack (list main technologies)
3. Complexity Level (Beginner/Intermediate/Advanced)
4. Key Features (bullet points)

Format your response as:
SUMMARY: <summary>
TECH_STACK: <technologies>
COMPLEXITY: <level>
FEATURES: <features>
"""
        return prompt
    
    @staticmethod
    def interview_prompt(project_context: Dict[str, Any], qa_history: list = None) -> str:
        """Generate prompt for interview agent"""
        summary = project_context.get("summary", "")
        tech_stack = project_context.get("tech_stack", "")
        complexity = project_context.get("complexity", "")
        
        qa_context = ""
        if qa_history:
            qa_context = "\n\nPrevious Q&A:\n"
            for qa in qa_history:
                qa_context += f"Q: {qa.get('question', '')}\nA: {qa.get('answer', '')}\n"
        
        prompt = f"""You are an expert technical interviewer. Based on the project information below, generate 3 relevant technical questions.

Project Summary: {summary}
Technology Stack: {tech_stack}
Complexity Level: {complexity}
{qa_context}

Generate 3 technical questions that:
- Test understanding of the technologies used
- Probe into design decisions
- Explore implementation details
- Are appropriate for the complexity level

Format as:
Q1: <question>
Q2: <question>
Q3: <question>
"""
        return prompt
    
    @staticmethod
    def followup_prompt(question: str, answer: str, project_context: Dict[str, Any]) -> str:
        """Generate prompt for follow-up question"""
        prompt = f"""You are an expert technical interviewer. Based on the student's answer, generate 1 relevant follow-up question.

Original Question: {question}
Student's Answer: {answer}

Generate a follow-up question that:
- Digs deeper into their understanding
- Clarifies vague points
- Explores edge cases or alternatives

Format as:
FOLLOWUP: <question>
"""
        return prompt
    
    @staticmethod
    def evaluation_prompt(project_context: Dict[str, Any], qa_history: list) -> str:
        """Generate prompt for evaluation agent"""
        summary = project_context.get("summary", "")
        
        qa_text = ""
        for i, qa in enumerate(qa_history, 1):
            qa_text += f"\nQ{i}: {qa.get('question', '')}\n"
            qa_text += f"A{i}: {qa.get('answer', '')}\n"
        
        prompt = f"""You are an expert evaluator. Score the student's interview performance.

Project: {summary}

Interview Transcript:
{qa_text}

Evaluate on:
1. Clarity (1-10): How clear and articulate were the answers?
2. Technical Depth (1-10): How deep was the technical understanding?
3. Completeness (1-10): How complete were the explanations?

Provide scores and detailed feedback.

Format as:
CLARITY: <score>
TECHNICAL_DEPTH: <score>
COMPLETENESS: <score>
FEEDBACK: <detailed feedback>
"""
        return prompt
