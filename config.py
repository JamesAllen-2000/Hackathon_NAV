import os
from dotenv import load_dotenv

load_dotenv()


LLM_API_TOKEN = os.getenv("GROQ_API_KEY", "")
LLM_API_URL = "https://api.groq.com/openai/v1/chat/completions"
LLM_MODEL_NAME = "llama-3.3-70b-versatile"  # Free, fast, and powerful



# LLM Configuration
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 500

# Interview Configuration
NUM_INITIAL_QUESTIONS = 3
NUM_FOLLOWUP_QUESTIONS = 2

# Scoring Configuration
SCORING_CRITERIA = {
    "clarity": {"weight": 0.3, "max": 10},
    "technical_depth": {"weight": 0.4, "max": 10},
    "completeness": {"weight": 0.3, "max": 10}
}


UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
