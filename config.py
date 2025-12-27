import os
from dotenv import load_dotenv

load_dotenv()

# LLM API Configuration - Using Groq (FREE and FAST!)
# Get your free API key from: https://console.groq.com/keys
LLM_API_TOKEN = os.getenv("GROQ_API_KEY", "")
LLM_API_URL = "https://api.groq.com/openai/v1/chat/completions"
LLM_MODEL_NAME = "llama-3.3-70b-versatile"  # Free, fast, and powerful

# Alternative free models you can use:
# "mixtral-8x7b-32768" - Good for long context
# "llama3-70b-8192" - Balanced performance
# "gemma2-9b-it" - Lightweight and fast

# Alternative models (can be switched)
# HUGGINGFACE_MODEL_URL = "https://router.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
# HUGGINGFACE_MODEL_URL = "https://router.huggingface.co/models/tiiuae/falcon-7b-instruct"

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

# File paths
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
