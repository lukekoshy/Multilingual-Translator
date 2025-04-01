from deep_translator import GoogleTranslator
from config import SUPPORTED_LANGUAGES

def translate_text(text, target_lang):
    """
    Translates the given text into the target language using Google Translate.
    
    :param text: Text to be translated.
    :param target_lang: Target language code (e.g., 'fr' for French).
    :return: Translated text or raises an exception on error.
    """
    if not text or not text.strip():
        raise ValueError("No text provided for translation.")
    
    if target_lang not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language code: {target_lang}")

    try:
        # Initialize the translator
        translator = GoogleTranslator(source='auto', target=target_lang)
        
        # Translate the text
        # deep_translator automatically handles chunking for long text
        translation = translator.translate(text.strip())
        
        if not translation:
            raise ValueError("Received empty translation")
            
        return translation
        
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")

if __name__ == "__main__":
    # Test the translator
    test_texts = [
        ("Hello, how are you?", "fr"),
        ("Bonjour, comment allez-vous?", "en"),
        ("¿Cómo estás?", "en")
    ]
    
    for text, lang in test_texts:
        try:
            translation = translate_text(text, lang)
            print(f"Original ({lang}): {text}")
            print(f"Translated: {translation}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")

