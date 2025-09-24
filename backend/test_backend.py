from utils.nlp import preprocess
from utils.classify import classify_email
from utils.response import generate_response

# Emails de teste
emails = [
    "Olá, preciso de ajuda com meu pedido.",  # português, produtivo
    "Hello, I need help with my request.",    # inglês, produtivo
    "Feliz Natal! Obrigado por tudo.",        # português, improdutivo
    "Thank you for your support!"             # inglês, improdutivo
]

for email in emails:
    clean_text = preprocess(email)
    category = classify_email(email)
    response = generate_response(category)
    
    print(f"Email: {email}")
    print(f"Texto limpo: {clean_text}")
    print(f"Categoria: {category}")
    print(f"Resposta sugerida: {response}")
    print("-" * 50)