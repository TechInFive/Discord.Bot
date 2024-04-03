import os
from openai import OpenAI
import requests

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

    def draw_image(self, prompt, quality="standard", response_format="url",
                   size = "1024x1024", style="natural"):
        response = self.client.images.generate(
            prompt=prompt,
            model="dall-e-3",
            quality=quality,
            response_format=response_format,
            size=size,
            style=style,
        )

        return response

    def create_variant(self, image, size="1024x1024"):
        response = self.client.images.create_variation(
            image=image,
            size=size,
            n=1,
        )

        return response

    def simple_completion_test(self):
        messages = [
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ];
        chat_completion = self.simple_completion(messages)
        print(chat_completion)

    def draw_image_test(self, message):
        prompt = f"I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: {message}"
        image_response = self.draw_image(prompt)
        print(image_response)

    def create_variant_url_test(self, image_url):
        # Send a GET request to the image URL
        response = requests.get(image_url)
        response.raise_for_status()
    
        image_content = response.content
        image_response = self.create_variant(image_content)
        print(image_response)

    def create_variant_local_test(self, image_path):
        image_content = open(image_path, "rb")
        image_response = self.create_variant(image_content)
        print(image_response)
