from utils.nlp import preprocess
from utils.translate_email import translate_email
from utils.gpt_classify import classify_with_gpt

def classify_email_ai(text:str) -> str:
    # Traduz o texto para o inglês, para melhor precisão da IA
    translated_text = translate_email(text)

    # Tratamento do texto
    clean_text = preprocess(translated_text)

    # Classifica o texto
    classify_text_response = classify_with_gpt(clean_text)
    
    # Retorna a classificação do texto de acordo com a IA
    return classify_text_response