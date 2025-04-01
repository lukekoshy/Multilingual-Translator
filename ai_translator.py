from openai import OpenAI
from config import SUPPORTED_LANGUAGES
import os

class AITranslator:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)

    def translate_text(self, text, target_lang):
        """
        Translates text using OpenAI's GPT model.
        
        :param text: Text to translate
        :param target_lang: Target language code (e.g., 'fr' for French)
        :return: Translated text
        """
        if not text or not text.strip():
            raise ValueError("No text provided for translation.")

        if target_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language code: {target_lang}")

        target_language_name = SUPPORTED_LANGUAGES[target_lang]
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a translator. Translate the following text to {target_language_name}. "
                                 "Only respond with the translation, nothing else."
                    },
                    {"role": "user", "content": text}
                ],
                temperature=0.3,  # Lower temperature for more consistent translations
                max_tokens=1000
            )
            
            translation = response.choices[0].message.content.strip()
            if not translation:
                raise ValueError("Received empty translation from OpenAI")
                
            return translation
            
        except Exception as e:
            raise Exception(f"OpenAI translation failed: {str(e)}")

if __name__ == "__main__":
    # Test the AI translator
    try:
        translator = AITranslator()
        test_texts = [
            ("Hello, how are you?", "fr"),
            ("I love programming", "es"),
            ("The weather is nice today", "de")
        ]
        
        for text, lang in test_texts:
            try:
                translation = translator.translate_text(text, lang)
                print(f"Original ({lang}): {text}")
                print(f"Translated: {translation}\n")
            except Exception as e:
                print(f"Error: {str(e)}\n")
                
    except Exception as e:
        print(f"Failed to initialize AI translator: {str(e)}") 