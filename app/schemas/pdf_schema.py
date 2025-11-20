from pydantic import BaseModel

class PDFRequest(BaseModel):
    usuario_id: int
