def generate_response(category: str) -> str:
    """
    Gera uma resposta automática baseada na categoria do email.
    Suporta português e inglês.
    """
    if category == "Produtivo":
        return "Recebemos seu email e vamos processar sua solicitação o mais rápido possível."
    elif category == "Improdutivo":
        return "Obrigado pelo contato! Sua mensagem foi recebida."
    else:
        return "Não conseguimos identificar a categoria do email."
