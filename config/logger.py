import logging
import json
import sys
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        }
        if hasattr(record, "extra_data"):
            log_record["extra"] = record.extra_data
        return json.dumps(log_record, ensure_ascii=False)

def setup_logger():
    logger = logging.getLogger("llm_service")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        
        file_handler = logging.FileHandler("app.log", encoding="utf-8")
        file_handler.setFormatter(JsonFormatter())
        logger.addHandler(file_handler)
        
    return logger

logger = setup_logger()