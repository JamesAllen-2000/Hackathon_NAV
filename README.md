#  AI-Driven Automated Interviewer

An intelligent interview system that captures your presentation via screen share and voice, then generates context-aware technical questions based on what you presented.

##  Features

-  **Browser-based screen capture** (every 10 seconds)
-  **Real-time voice transcription** using Web Speech API
-  **AI-powered question generation** based on your presentation
-  **Voice-based Q&A** - Answer questions by speaking
-  **Automated evaluation** with detailed feedback
-  **Zero lag** - All processing happens after capture

##  Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Free Groq API Key
1. Go to: https://console.groq.com/keys
2. Sign up (free, no credit card)
3. Create API Key
4. Copy it

### 3. Configure
Open `.env` and add your key:
```
GROQ_API_KEY=gsk_your_key_here
```

### 4. Run
```bash
python app.py
```

Open http://127.0.0.1:5000 in **Chrome** browser

##  How to Use

1. **Start Presentation**
   - Click "Start Presentation"
   - Allow screen share (select your presentation window)
   - Allow microphone access

2. **Present**
   - Present for 1-2 minutes
   - System captures screen every 10 seconds
   - Voice transcription appears live
   - Click "Stop & Analyze" when done

3. **Interview**
   - AI generates questions based on your presentation
   - Click " Start Voice Answer" to speak your answer
   - Or type your answer
   - Submit to move to next question

4. **Evaluation**
   - Get scored on clarity, technical depth, and completeness
   - Receive detailed feedback

##  Project Structure

```
Hackathon/
├── app.py                          # Main Flask application
├── config.py                       # Configuration (API keys, models)
├── .env                            # Environment variables
├── requirements.txt                # Python dependencies
├── agents/                         # AI agents
│   ├── perception_agent.py        # Screen & audio processing
│   ├── understanding_agent.py     # Context analysis
│   ├── interview_agent.py         # Question generation
│   └── evaluation_agent.py        # Performance scoring
├── utils/                          # Utilities
│   ├── ocr_handler.py             # Screen text extraction (EasyOCR)
│   └── llm_client.py              # LLM API wrapper (Groq)
└── templates/
    └── index.html                  # Frontend UI

```

##  Configuration

### LLM Models
Edit `config.py` to change models:

```python
LLM_MODEL_NAME = "llama-3.3-70b-versatile"  # Default (best)

# Alternatives:
# "mixtral-8x7b-32768" - Long context
# "llama3-70b-8192" - Balanced
# "gemma2-9b-it" - Fastest
```

### Capture Settings
```python
# config.py
NUM_INITIAL_QUESTIONS = 3           # Number of questions
SCORING_CRITERIA = {
    "clarity": {"weight": 0.3},
    "technical_depth": {"weight": 0.4},
    "completeness": {"weight": 0.3}
}
```

##  Tech Stack

- **Backend**: Flask + Python
- **Frontend**: HTML/CSS/JavaScript
- **OCR**: EasyOCR (CPU-based)
- **Speech**: Web Speech API (Chrome)
- **LLM**: Groq API (Llama 3.3 70B)
- **Image Processing**: Pillow

##  Free APIs Used

- **Groq**: 14,400 requests/day, 30K tokens/min (FREE!)
- **Web Speech API**: Built into Chrome (FREE!)
- **EasyOCR**: Local CPU processing (FREE!)
