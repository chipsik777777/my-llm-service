class PromptBuilder:
    @staticmethod
    def build_messages(user_message: str, system_instruction: str = "Ты — полезный ассистент. Ответь кратко и четко."):
        return [
            {"role": "system", "content": system_instruction.strip()},
            {"role": "user", "content": user_message.strip()}
        ]