from fastapi import UploadFile, HTTPException
from PyPDF2 import PdfReader

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

async def extract_text(file: UploadFile) -> str:
    """
    Valida e extrai texto de arquivos suportados (.pdf, .txt) com verificações de tamanho.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Arquivo sem nome.")

    filename = file.filename.lower()

    # Verifica extensão
    if not (filename.endswith(".pdf") or filename.endswith(".txt")):
        raise HTTPException(
            status_code=400,
            detail="Formato de arquivo não suportado. Apenas PDF e TXT são aceitos."
        )

    # Checa tamanho
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"O arquivo excede o tamanho máximo de {MAX_FILE_SIZE // (1024*1024)} MB."
        )
    await file.seek(0)  # reseta ponteiro para leitura posterior

    # PDF
    if filename.endswith(".pdf"):
        try:
            reader = PdfReader(file.file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            if not text.strip():
                raise HTTPException(status_code=400, detail="Arquivo PDF vazio ou ilegível.")
            return text.strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao processar PDF: {str(e)}")

    # TXT
    if filename.endswith(".txt"):
        try:
            content = await file.read()
            text = content.decode("utf-8")
            if not text.strip():
                raise HTTPException(status_code=400, detail="Arquivo TXT vazio ou ilegível.")
            return text.strip()
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Erro ao decodificar TXT. Use UTF-8.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao processar TXT: {str(e)}")