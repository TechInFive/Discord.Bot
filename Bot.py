import os
import random
import discord

from ChatService import ChatService

# Jokes
python_jokes = [
    "Why do Python programmers prefer dark mode? Because light attracts bugs.",
    "Why was the Python developer not responding? Because he was in a deadlock.",
    "How do you make a Python script stand up? You can't; it's always a 'script'.",
    "Why did the Python programmer get rejected on a date? Because he didn't understand Java.",
    "What do you call a snake that programs in Python? A Pyth-on-coder."
]

BOT_TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents.default()  # Default intents
intents.messages = True  # Enable message events
intents.guild_messages = True  # Enable guild (server) message events
intents.message_content = True  # Enable message content

# Initialize the client with the defined intents
client = discord.Client(intents=intents)

# Setting a custom prefix
custom_prefix = "!"

chat_service = ChatService()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # Don't let the bot respond to its own messages
    if message.author == client.user:
        return

    print(message.content)

    if not message.content.startswith(custom_prefix):
        return

    if message.content.startswith("!joke"):
        joke = random.choice(python_jokes)
        await message.channel.send(joke)
    elif message.content == "!modelinfo":
        model_info = (
            "**AI Model Information:**\n"
            "- OpenAI GPT-4: The latest generative model, ideal for complex queries.\n"
            "- Mistral AI: Specialized in concise responses, perfect for quick facts."
        )
        await message.channel.send(model_info)
    elif message.content == "!help":
        help_text = (
            "**Bot Commands:**\n"
            "- `!openai <query>`: Get responses from OpenAI.\n"
            "- `!mistral <query>`: Get responses from Mistral AI.\n"
            "- `!joke`: Display a Python Joke.\n"
            "- `!modelinfo`: Get information about the AI models.\n"
            "- `!help`: Display this help message."
        )
        await message.channel.send(help_text)
    else:
        response_text = chat_service.handle_message(message.content)
        if response_text != None:
            await message.channel.send(response_text)

client.run(BOT_TOKEN)
