import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

class MistralAIService():
    def __init__(self):
        self.client = MistralClient(
            api_key=os.environ.get("MISTRAL_API_KEY"),
        )

        # model: https://docs.mistral.ai/platform/endpoints/
        self.model = "mistral-large-latest"

    def simple_completion(self, messages):
        chat_response = self.client.chat(
            messages=messages,
            model=self.model,
        )

        return chat_response

    def simple_completion_test(self):
        messages = [
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ];
        chat_completion = self.simple_completion(messages)
        print(chat_completion)


service = MistralAIService()
service.simple_completion_test()
