from flask import Flask, render_template, jsonify, request, session
from flask_cors import CORS
import os
import base64
from PIL import Image
import io
from agents import UnderstandingAgent, InterviewAgent, EvaluationAgent
from utils import OCRHandler
import uuid
import threading

app = Flask(__name__)
app.secret_key = 'hackathon-ai-interviewer-2025'
CORS(app)

# Session storage
sessions = {}

def get_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def get_session_data():
    session_id = get_session_id()
    if session_id not in sessions:
        sessions[session_id] = {
            'screen_images': [],
            'audio_files': [],
            'screen_texts': [],
            'audio_transcripts': [],
            'project_context': None,
            'questions': [],
            'answers': [],
            'stage': 'idle',
            'processing': False
        }
    return sessions[session_id]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/capture/screen', methods=['POST'])
def capture_screen():
    """Just save screen image - no OCR yet"""
    data = get_session_data()
    
    try:
        image_data = request.json.get('image')
        if image_data:
            # Just store base64 - don't process yet
            data['screen_images'].append(image_data)
            return jsonify({
                'success': True,
                'count': len(data['screen_images'])
            })
        return jsonify({'success': False}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/capture/audio', methods=['POST'])
def capture_audio():
    """Legacy endpoint - kept for compatibility"""
    return jsonify({'success': True, 'count': 0})

@app.route('/api/capture/transcript', methods=['POST'])
def capture_transcript():
    """Receive live transcript from Web Speech API"""
    data = get_session_data()
    
    try:
        text = request.json.get('text')
        if text and len(text.strip()) > 0:
            data['audio_transcripts'].append({'text': text.strip()})
            return jsonify({
                'success': True,
                'count': len(data['audio_transcripts'])
            })
        return jsonify({'success': False}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/process', methods=['POST'])
def process_all():
    """Process everything after capture stops"""
    data = get_session_data()
    
    if data['processing']:
        return jsonify({'success': False, 'error': 'Already processing'}), 400
    
    data['processing'] = True
    
    # Process in background thread
    def process():
        try:
            # Initialize OCR handler only (transcripts come from browser)
            ocr_handler = OCRHandler()
            
            # Process screens
            print(f"Processing {len(data['screen_images'])} screens...")
            for i, img_data in enumerate(data['screen_images']):
                img_data = img_data.split(',')[1] if ',' in img_data else img_data
                img_bytes = base64.b64decode(img_data)
                image = Image.open(io.BytesIO(img_bytes))
                
                text = ocr_handler.extract_text_from_pil_image(image)
                if text and len(text) > 10:
                    data['screen_texts'].append({'text': text})
                print(f"  Screen {i+1}/{len(data['screen_images'])} done")
            
            # Audio transcripts already collected via Web Speech API
            print(f"Audio transcripts: {len(data['audio_transcripts'])} segments received")
            
            # Combine context
            screen_text = '\n\n'.join([f"[{i+1}] {t['text']}" for i, t in enumerate(data['screen_texts'])])
            audio_text = '\n\n'.join([f"[{i+1}] {t['text']}" for i, t in enumerate(data['audio_transcripts'])])
            
            print(f"✓ Extracted text from {len(data['screen_texts'])} screens")
            print(f"✓ Transcribed {len(data['audio_transcripts'])} audio segments")
            
            perception_data = {
                'screen_text': screen_text,
                'audio_transcript': audio_text if audio_text else "[No audio transcription available]"
            }
            
            # Understanding Agent
            print("Analyzing context...")
            understanding_agent = UnderstandingAgent()
            data['project_context'] = understanding_agent.understand(perception_data)
            
            # Interview Agent
            print("Generating questions...")
            interview_agent = InterviewAgent()
            data['questions'] = interview_agent.generate_initial_questions(data['project_context'])
            
            data['stage'] = 'interview'
            data['processing'] = False
            print("Done!")
            
        except Exception as e:
            import traceback
            print(f"\n=== ERROR ===")
            print(traceback.format_exc())
            print(f"=============")
            data['processing'] = False
            data['error'] = str(e)
    
    thread = threading.Thread(target=process, daemon=True)
    thread.start()
    
    return jsonify({'success': True, 'message': 'Processing started'})

@app.route('/api/status', methods=['GET'])
def get_status():
    data = get_session_data()
    return jsonify({
        'stage': data['stage'],
        'screen_captures': len(data['screen_images']),
        'audio_segments': len(data['audio_files']),
        'processing': data['processing'],
        'ready': len(data['screen_images']) >= 2 or len(data['audio_files']) >= 2
    })

@app.route('/api/get-questions', methods=['GET'])
def get_questions():
    data = get_session_data()
    return jsonify({'questions': data['questions']})

@app.route('/api/answer', methods=['POST'])
def submit_answer():
    data = get_session_data()
    try:
        req_data = request.json
        idx = req_data.get('question_idx')
        answer = req_data.get('answer')
        
        data['answers'].append({
            'question': data['questions'][idx],
            'answer': answer
        })
        
        is_last = idx >= len(data['questions']) - 1
        return jsonify({'success': True, 'is_last': is_last})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    data = get_session_data()
    try:
        eval_agent = EvaluationAgent()
        evaluation = eval_agent.evaluate(data['project_context'], data['answers'])
        data['stage'] = 'evaluation'
        return jsonify({'success': True, 'evaluation': evaluation})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset():
    session_id = get_session_id()
    if session_id in sessions:
        # Cleanup audio files
        for filepath in sessions[session_id].get('audio_files', []):
            if os.path.exists(filepath):
                os.remove(filepath)
        del sessions[session_id]
    return jsonify({'success': True})

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('temp_audio', exist_ok=True)
    # Disable auto-reloader so background threads aren't killed
    app.run(debug=True, port=5000, host='127.0.0.1', threaded=True, use_reloader=False)
