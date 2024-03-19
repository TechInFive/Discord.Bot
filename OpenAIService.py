import os
from openai import OpenAI

class OpenAIService():
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        # model: https://platform.openai.com/docs/models/gpt-3-5-turbo
        # model: https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo
        self.model = "gpt-4-turbo-preview"

    def simple_completion(self, messages):
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
        )

        return chat_completion

    def simple_completion_test(self):
        messages = [
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ];
        chat_completion = self.simple_completion(messages)
        print(chat_completion)


service = OpenAIService()
service.simple_completion_test()
