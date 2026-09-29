from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from api.router import router as api_router

app = FastAPI(
    title="LLM Service Production Ready",
    description="Сервис с поддержкой кеширования, ретраев и fallback.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "service": "LLM Service Pipeline"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)