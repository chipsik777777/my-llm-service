import os
import time
import httpx
from config.logger import logger

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        self.timeout = 5.0
        self.max_retries = 3

    def generate(self, messages: list, model: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"Запрос к LLM (Попытка {attempt}/{self.max_retries})")
                start_time = time.time()
                
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
                    response.raise_for_status()
                    data = response.json()
                    
                elapsed = round(time.time() - start_time, 3)
                logger.info(f"Успешный ответ LLM за {elapsed}s")
                
                raw_text = data["choices"][0]["message"]["content"]
                return raw_text.strip()

            except (httpx.TimeoutException, httpx.HTTPStatusError, httpx.RequestError) as e:
                logger.error(f"Ошибка вызова LLM на попытке {attempt}: {str(e)}")
                if attempt < self.max_retries:
                    sleep_time = 2 ** attempt
                    time.sleep(sleep_time)
                else:
                    logger.warning("Все попытки исчерпаны. Активация Fallback-ответа.")
                    return self._fallback_response()

    def _fallback_response(self) -> str:
        return "Сервис временно недоступен. Пожалуйста, повторите попытку позже."

llm_client = LLMClient()