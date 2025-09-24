from utils.nlp import preprocess

def classify_email(text: str) -> str:
    """
    Classifica email como Produtivo ou Improdutivo
    usando palavras-chave em português ou inglês.
    """
    text_clean = preprocess(text)

    # Palavras-chave em ambos os idiomas
    keywords = [
        "solicitação", "problema", "ajuda", "erro", "suporte",   # português
        "request", "issue", "problem", "help", "support"         # inglês
    ]

    if any(word in text_clean for word in keywords):
        return "Produtivo"
    return "Improdutivo"
