import time
from cache.memory_cache import cache_instance
from llm.prompt import PromptBuilder
from llm.client import llm_client

class PipelineService:
    def process_request(self, message: str, system_instruction: str, model: str = "gpt-4o-mini", temperature: float = 0.7) -> dict:
        start_time = time.time()
        
        # 1. Проверка кеша
        cached_result = cache_instance.get(message, model, temperature, system_instruction)
        if cached_result:
            return {
                "result": cached_result,
                "cached": True,
                "execution_time_sec": round(time.time() - start_time, 3)
            }

        # 2. Формирование промпта
        messages = PromptBuilder.build_messages(message, system_instruction)

        # 3. Вызов LLM
        llm_response = llm_client.generate(messages, model=model, temperature=temperature)

        # 4. Сохранение в кеш
        if "Сервис временно недоступен" not in llm_response:
            cache_instance.set(message, model, temperature, system_instruction, llm_response)

        return {
            "result": llm_response,
            "cached": False,
            "execution_time_sec": round(time.time() - start_time, 3)
        }

pipeline_service = PipelineService()