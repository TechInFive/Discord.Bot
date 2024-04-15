import os
import random
import discord

from ChatService import ChatService
from OpenAIService import OpenAIService

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

# Attempt to load the Opus library
if not discord.opus.is_loaded():
    # The name of the Opus library may vary depending on your system
    # Windows: opus.dll
    # macOS: libopus.dylib
    # Linux: libopus.so
    discord.opus.load_opus(os.getenv('LIBOPUS_PATH'))

chat_service = ChatService()
open_ai_service = OpenAIService()

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
            "**Bot Commands Overview:**\n"
            "- `!openai <query>`: Query OpenAI's models for detailed responses to complex questions.\n"
            "- `!mistral <query>`: Access Mistral AI for quick, concise answers to your inquiries.\n"
            "- `!dall-e <query>`: Use DALL-E to create images based on your textual descriptions.\n"
            "- `!join`: Commands the bot to join the voice channel you are currently in.\n"
            "- `!leave`: Instructs the bot to leave the current voice channel, ending any active participation.\n"
            "- `!joke`: Enjoy a light-hearted Python joke to brighten your day.\n"
            "- `!modelinfo`: Learn about the AI models powering the bot, including their features and uses.\n"
            "- `!permissions`: Displays the bot’s permissions for transparency and trust.\n"
            "- `!help`: Provides this message, listing all available commands and their functions.\n"
            "Use these commands to enhance your interaction with the bot and explore its functionalities."
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

    elif content == "!join":
        # Check if the bot is already in a voice channel in this guild
        if message.guild.voice_client is not None:
            await message.channel.send("I'm already in a voice channel.")
            return

        # Check if the user is in a voice channel
        if message.author.voice and message.author.voice.channel:
            voice_channel = message.author.voice.channel
            await voice_channel.connect()
            await message.channel.send(f"Joined {voice_channel.name}!")
        else:
            await message.channel.send("You need to be in a voice channel for me to join.")

    elif content == "!leave":
        # Check if the bot is in a voice channel in this guild
        if message.guild.voice_client is not None:
            await message.guild.voice_client.disconnect()
            await message.channel.send("I've left the voice channel.")
        else:
            await message.channel.send("I'm not in any voice channel right now.")

    else:
        response_text = chat_service.handle_message(channel.id, content)
        if response_text != None:
            await channel.send(response_text)

            # Check if the user is in a voice channel
            if message.author.voice and message.author.voice.channel:
                # Check if the bot is in a voice channel in this guild
                if message.guild.voice_client is not None:
                    open_ai_service.create_speech_file("echo", response_text, "ai_response.mp3")

                    source = discord.FFmpegPCMAudio("ai_response.mp3")
                    message.guild.voice_client.play(source, after=lambda e: print('Finished playing', e))

client.run(BOT_TOKEN)
