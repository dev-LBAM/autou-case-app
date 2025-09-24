from utils.gpt_response import generate_response_with_gpt

def reply_email_ai(email_text: str, category: str) -> str:
    # Gera uma resposta de acordo com o texto + categoria
    response = generate_response_with_gpt(email_text, category)
    
    # Retorna a resposta gerada pela IA
    return response