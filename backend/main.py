from fastapi import FastAPI
from pydantic import BaseModel
from utils.classify import classify_email
from utils.response import generate_response

app = FastAPI(title="AutoU Email Classifier")

# Modelo de dados do email
class Email(BaseModel):
    content: str

# Endpoint raiz para teste
@app.get("/")
def read_root():
    return {"message": "API do AutoU Backend funcionando!"}

# Endpoint para processar email
@app.post("/process_email")
def process_email(email: Email):
    category = classify_email(email.content)
    response = generate_response(category)
    return {
        "category": category,
        "suggested_response": response
    }
