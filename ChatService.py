from MistralAIService import MistralAIService
from OpenAIService import OpenAIService

class ChatService:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.mistral_service = MistralAIService()

    def handle_message(self, message):
        if message.startswith("!openai"):
            # Remove command from message to pass only the user's query
            query = message[len("!openai"):].strip()
            messages = [{"role": "user", "content": query}]
            response = self.openai_service.simple_completion(messages)
            return response.choices[0].message.content

        if message.startswith("!mistral"):
            query = message[len("!mistral"):].strip()
            messages = [{"role": "user", "content": query}]
            response = self.mistral_service.simple_completion(messages)
            return response.choices[0].message.content

        return None
