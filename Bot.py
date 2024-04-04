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

    # Focus on text channels and public threads
    if message.channel.type not in [discord.ChannelType.text, discord.ChannelType.public_thread]:
        return

    # Ignore unsupported message types
    if message.type not in [discord.MessageType.default, discord.MessageType.reply]:
        return

    # text - Test message @ 845081847410065418
    # private - Test DM @ 1219276778581790770
    # public_thread - Test Thread Replay @ 1222276084905803908
    # public_thread Test Reply of Thread Message @ 1222276084905803908
    # text - Test - Reply Channel Message @ 845081847410065418
    # text - Test - Reply Channel Message @ 845081847410065418
    # text - Create new thread @ 845081847410065418
    # public_thread - First message of new thread @ 1222285886998446201

    # MessageType.default
    # MessageType.reply
    # MessageType.thread_created
    
    content = message.content
    channel = message.channel

    if content == "!joke":
        joke = random.choice(python_jokes)
        await channel.send(joke)
    elif content == "!modelinfo":
        model_info = (
            "**AI Model Information:**\n"
            "- OpenAI GPT-4: The latest generative model, ideal for complex queries.\n"
            "- Mistral AI: Specialized in concise responses, perfect for quick facts."
        )
        await channel.send(model_info)
    elif content == "!help":
        help_text = (
            "**Bot Commands:**\n"
            "- `!openai <query>`: Get responses from OpenAI.\n"
            "- `!mistral <query>`: Get responses from Mistral AI.\n"
            "- `!joke`: Display a Python Joke.\n"
            "- `!modelinfo`: Get information about the AI models.\n"
            "- `!help`: Display this help message."
        )
        await channel.send(help_text)
    elif content == "!permissions":
        bot_member = message.guild.get_member(client.user.id)
        perms_list = [f"{perm[0]}: {perm[1]}" for perm in bot_member.guild_permissions]
        perms_str = "\n".join(perms_list)
        await channel.send(f"Permissions for the bot:\n```\n{perms_str}\n```")

        channel_permissions = channel.permissions_for(message.guild.me)
        perms_list = [f"{perm[0]}: {perm[1]}" for perm in channel_permissions]
        perms_str = "\n".join(perms_list)
        await channel.send(f"Permissions in this channel:\n```\n{perms_str}\n```")

    elif content.startswith("!dall-e"):
        response_text = chat_service.draw_image(content)
        await channel.send(response_text)
    else:
        response_text = chat_service.handle_message(channel.id, content)
        if response_text != None:
            await channel.send(response_text)

client.run(BOT_TOKEN)
