import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from langdetect import detect

# Baixar recursos
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

def preprocess(text: str) -> str:
    """
    Limpa o texto e remove stopwords do idioma detectado.
    Suporta português e inglês.
    """
    # Detecta idioma
    lang = detect(text)
    
    words = word_tokenize(text.lower())
    
    # Escolhe stopwords de acordo com o idioma
    if lang == 'pt':
        stop_words = stopwords.words('portuguese')
    else:
        stop_words = stopwords.words('english')
    
    words = [w for w in words if w.isalpha() and w not in stop_words]
    return ' '.join(words)