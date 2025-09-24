from deep_translator import GoogleTranslator

def translate_email(text: str) -> str:
    """
    Traduz texto para inglês usando Deep Translator.
    """
    translated_text = GoogleTranslator(source='auto', target='en').translate(text)
    return translated_text
