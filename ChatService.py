from discord import Embed
from MistralAIService import MistralAIService
from OpenAIService import OpenAIService

class ChatService:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.mistral_service = MistralAIService()
        self.conversations = {}  # Dictionary to store conversation history

    def handle_message(self, channel_id, message):
        # Determine AI service based on the command
        service = None
        query = None
        if message.startswith("!openai"):
            service = self.openai_service
            query = message[len("!openai"):].strip()
        elif message.startswith("!mistral"):
            service = self.mistral_service
            query = message[len("!mistral"):].strip()

        if service == None:
            return None

        # Initialize conversation history with a system message if not already present
        if channel_id not in self.conversations:
            self.conversations[channel_id] = [{
                "role": "system",
                "content": "Please generate a response with less than 1000 characters to accommodate Discord's character limit."
            }]
        conversations = self.conversations[channel_id]

        # Keep the conversation history within a manageable size
        if len(conversations) > 10:
            # always retaining the first system message
            conversations = [conversations[0]] + conversations[-9:]
            self.conversations[channel_id] = conversations

        user_message = {"role": "user", "content": query}

        # Add user message to the conversation history
        conversations.append(user_message)

        messages = conversations
        response = service.simple_completion(messages)
        response_content = response.choices[0].message.content

        ai_response = {"role": "assistant", "content": response_content}
        conversations.append(ai_response)

        return response_content


    def draw_image(self, message):
        if not message.startswith("!dall-e"):
            return None

        message = message[len("!dall-e"):].strip()

        chat_prompt = "Please create prompt for DALL-E 3. Requirement is : " + message
        system_message = """Generate an improved prompt for an image description to be used with DALL-E 3.
                         The prompt should be concise, evocative, and designed to yield visually compelling
                         results. Do not provide explanations or additional context; focus only on creating
                         the prompt itself."""

        messages = [
           {
               "role": "system",
               "content": system_message
           },
           {
               "role": "user",
                "content": chat_prompt
           },
        ]

        response = self.openai_service.simple_completion(messages)
        response_content = response.choices[0].message.content
        print(response_content)

        image_response = self.openai_service.draw_image(response_content, style="vivid")
        return image_response.data[0].url
