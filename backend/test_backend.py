from utils.nlp import preprocess
from utils.translate_email import translate_email
from utils.ai_respondent import reply_email_ai
from utils.ai_classifier import classify_email_ai

# Emails de teste
emails = [
    "Olá, preciso de ajuda com meu pedido.",  # português, produtivo
    "Hello, I need help with my request.",    # inglês, produtivo
    "Feliz Natal! Obrigado por tudo.",        # português, improdutivo
    "Thank you for your support!",         # inglês, improdutivo
    "Olá equipe, estou com problema para acessar minha conta, preciso de ajuda urgente.", # português, produtivo
    "Feliz aniversário a todos! Que tenham um ótimo dia!" # português, improdutivo
]

for email in emails:
    translate_text = translate_email(email)
    clean_text = preprocess(translate_text)
    ai_category = classify_email_ai(email)
    response = reply_email_ai(email, ai_category)
    
    print("-" * 50)
    print(f"Email: {email}")
    print(f"Texto Traduzido: {translate_text}")
    print(f"Texto limpo: {clean_text}")
    print(f"Categoria sugerida pela IA: {ai_category}\n")
    print(f"Resposta sugerida pela IA: {response}")
    print("-" * 50)