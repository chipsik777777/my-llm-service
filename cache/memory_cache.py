import hashlib
import time
from typing import Optional, Dict, Any
from config.logger import logger

class MemoryCache:
    def __init__(self, default_ttl: int = 600):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl

    def _generate_key(self, message: str, model: str, temperature: float, system_prompt: str) -> str:
        raw_string = f"{message}:{model}:{temperature}:{system_prompt}"
        return hashlib.sha256(raw_string.encode("utf-8")).hexdigest()

    def get(self, message: str, model: str, temperature: float, system_prompt: str) -> Optional[str]:
        key = self._generate_key(message, model, temperature, system_prompt)
        item = self._cache.get(key)
        
        if not item:
            logger.info("CACHE MISS", extra={"extra_data": {"cache_key": key}})
            return None
            
        if time.time() > item["expires_at"]:
            del self._cache[key]
            logger.info("CACHE EXPIRED", extra={"extra_data": {"cache_key": key}})
            return None
            
        logger.info("CACHE HIT", extra={"extra_data": {"cache_key": key}})
        return item["value"]

    def set(self, message: str, model: str, temperature: float, system_prompt: str, value: str, ttl: Optional[int] = None):
        key = self._generate_key(message, model, temperature, system_prompt)
        expire_time = time.time() + (ttl if ttl is not None else self.default_ttl)
        self._cache[key] = {
            "value": value,
            "expires_at": expire_time
        }
        logger.info("CACHE STORED", extra={"extra_data": {"cache_key": key, "ttl": ttl or self.default_ttl}})

cache_instance = MemoryCache()