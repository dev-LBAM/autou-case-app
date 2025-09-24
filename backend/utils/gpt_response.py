import os
from dotenv import load_dotenv
from openai import OpenAI

# Carrega variáveis do .env
load_dotenv()

# Conecta com a IA
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response_with_gpt(email_text: str, category: str) -> str:
    """
    Gera uma resposta adequada ao email, considerando a categoria.
    """
    if category == "Produtivo":
        tone = "profissional e rápida"
    else:
        tone = "cordial e amigável"

    prompt = f"""
    Você é um assistente que responde emails de clientes de forma {tone}.
    Email: "{email_text}"
    Responda de forma concisa e adequada.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    answer = response.choices[0].message.content.strip()
    return answer