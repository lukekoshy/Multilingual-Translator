from flask import Flask, request, jsonify
from flask_cors import CORS
from translator import translate_text as google_translate
from ai_translator import AITranslator
from config import SUPPORTED_LANGUAGES
import os
from dotenv import load_dotenv
d
# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS to allow requests from all frontend development ports
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5173",
            "http://localhost:5174",
            "http://localhost:5175",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            "http://127.0.0.1:5175"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Initialize AI translator
ai_translator = None
try:
    if os.getenv('OPENAI_API_KEY'):
        ai_translator = AITranslator()
    else:
        print("Warning: OPENAI_API_KEY is not set in the environment variables")
except Exception as e:
    print(f"Warning: Failed to initialize AI translator: {str(e)}")

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    text = data.get('text')
    target_lang = data.get('target_lang')
    service = data.get('service', 'google')  # default to google translate

    if not text or not target_lang:
        return jsonify({'error': 'Missing required parameters: text and target_lang'}), 400

    if target_lang not in SUPPORTED_LANGUAGES:
        return jsonify({
            'error': f'Unsupported language: {target_lang}. Supported languages are: {", ".join(SUPPORTED_LANGUAGES.keys())}'
        }), 400

    try:
        if service == 'openai':
            if not ai_translator:
                return jsonify({'error': 'OpenAI translation service is not available'}), 503
            translation = ai_translator.translate_text(text, target_lang)
        else:
            translation = google_translate(text, target_lang)
        
        return jsonify({
            'original_text': text,
            'translated_text': translation,
            'target_language': target_lang,
            'target_language_name': SUPPORTED_LANGUAGES[target_lang],
            'service': service
        })
    except Exception as e:
        error_message = str(e)
        print(f"Translation error: {error_message}")  # Log the error
        return jsonify({'error': f'Translation failed: {error_message}'}), 500

@app.route('/languages', methods=['GET'])
def get_languages():
    return jsonify({
        'languages': {
            code: name for code, name in SUPPORTED_LANGUAGES.items()
        },
        'services': ['google', 'openai'] if ai_translator else ['google']
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'services': {
            'google': True,
            'openai': ai_translator is not None
        },
        'supported_languages_count': len(SUPPORTED_LANGUAGES)
    })

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
