# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from utils.ai_classifier import classify_email_ai
from utils.ai_respondent import reply_email_ai
from utils.file_extraction import extract_text

app = FastAPI(title="AutoU Email Classifier")

class EmailContent(BaseModel):
    content: str

    class Config:
        json_schema_extra = {
            "example": {
                "content": "Olá, preciso de ajuda para acessar minha conta. Não consigo conectar desde ontem."
            }
        }

class SuccessResponse(BaseModel):
    category: str
    suggested_response: str

# -------- Endpoint JSON --------
@app.post("/process_email", response_model=SuccessResponse, status_code=200)
async def process_email_json(email: EmailContent):
    """
    Recebe JSON com { content: "..." }.
    """
    text = email.content
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Campo 'content' vazio.")

    category = classify_email_ai(text)
    response = reply_email_ai(text, category)
    return SuccessResponse(category=category, suggested_response=response)

# -------- Endpoint arquivo --------
@app.post("/process_email/file", response_model=SuccessResponse, status_code=200)
async def process_email_file(file: UploadFile = File(..., description="Envie um arquivo .txt ou .pdf até 5MB")):
    """
    Recebe um arquivo .pdf ou .txt.
    """
    try:
        text = await extract_text(file)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro inesperado ao processar arquivo: {e}")

    category = classify_email_ai(text)
    response = reply_email_ai(text, category)
    return SuccessResponse(category=category, suggested_response=response)