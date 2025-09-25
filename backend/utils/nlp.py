import re
import nltk
from nltk.data import find
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Função para garantir que os recursos necessários estejam baixados
def download_nltk_resources():
    resources = ["punkt_tab", "punkt", "stopwords", "wordnet", "omw-1.4"]
    for resource in resources:
        try:
            find(f"corpora/{resource}")
        except LookupError:
            nltk.download(resource)

download_nltk_resources()

lemmatizer = WordNetLemmatizer()
stop_words_en = set(stopwords.words("english"))

def preprocess(text: str) -> str:
    """
    Pré-processa texto em inglês:
    - minúsculas
    - remove URLs, emails e números
    - remove pontuação
    - tokeniza
    - remove stop words
    - aplica lematização
    """
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)   # URLs
    text = re.sub(r"\S+@\S+", " ", text)                   # emails
    text = re.sub(r"\d+", " ", text)                       # números
    text = re.sub(r"[^\w\s]", " ", text)                   # pontuação (!, ?, ., , etc.)
    text = re.sub(r"[_]", " ", text)                       # underline ou resquícios

    words = nltk.word_tokenize(text, language="english")
    words = [w for w in words if w not in stop_words_en]
    words = [lemmatizer.lemmatize(w) for w in words]

    return " ".join(words)