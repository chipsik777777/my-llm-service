from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from services.pipeline import pipeline_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="Сообщение пользователя")
    system_instruction: str = Field(default="Ты — полезный ассистент.", max_length=500)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

class ChatResponse(BaseModel):
    status: str
    result: str
    cached: bool
    execution_time_sec: float

@router.post("/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    try:
        data = pipeline_service.process_request(
            message=request.message,
            system_instruction=request.system_instruction,
            temperature=request.temperature
        )
        return ChatResponse(
            status="success",
            result=data["result"],
            cached=data["cached"],
            execution_time_sec=data["execution_time_sec"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервиса: {str(e)}")