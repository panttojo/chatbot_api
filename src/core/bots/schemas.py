from pydantic import BaseModel


class ChatErrorResponse(BaseModel):
    output_text: str
