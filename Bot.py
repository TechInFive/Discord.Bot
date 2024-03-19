import os
import random
import discord

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

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # Don't let the bot respond to its own messages
    if message.author == client.user:
        return

    # Check if the bot is mentioned in the message
    if client.user.mentioned_in(message):
        # Reply with "Hello <author>"
        await message.channel.send(f'Hello {message.author.name}!')
        # await message.channel.send(f'Hello TechInFive!')

    if message.content.startswith("!joke"):
        joke = random.choice(python_jokes)
        print(joke)
        await message.channel.send(joke)

client.run(BOT_TOKEN)
