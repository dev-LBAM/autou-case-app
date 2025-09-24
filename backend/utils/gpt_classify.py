import os
from dotenv import load_dotenv
from openai import OpenAI

# Carrega variáveis do .env
load_dotenv()

# Conecta com a IA
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_with_gpt(email_text: str) -> str:
    """
    Classifica o email como 'Produtivo' ou 'Improdutivo'.
    """
    prompt = f"""
    Classifique o seguinte email em uma das duas categorias: Produtivo ou Improdutivo.
    Produtivo = Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
    Improdutivo = Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).
    Email: "{email_text}"
    Retorne apenas a categoria.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10
    )
    category = response.choices[0].message.content.strip()
    return category