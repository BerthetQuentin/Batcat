import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# Load the .env file
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Configure the intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.members = True

# Create the bot with a command prefix
bot = commands.Bot(command_prefix='+', intents=intents)

# Define an asynchronous setup function
async def setup_extensions():
    await bot.load_extension('cogs.moderation')
    await bot.load_extension('cogs.reactions')
    await bot.load_extension('cogs.spam')
    await bot.load_extension('cogs.logging')
    await bot.load_extension('cogs.test')

@bot.event
async def on_ready():
    print("\033[91m" + r"""
__________    _________________________     ________________
\______   \  /  _  \__    ___/\_   ___ \   /  _  \__    ___/
 |    |  _/ /  /_\  \|    |   /    \  \/  /  /_\  \|    |   
 |    |   \/    |    \    |   \     \____/    |    \    |   
 |______  /\____|__  /____|    \______  /\____|__  /____|   
        \/         \/                 \/         \/         
    """)

    print("\033[91m" + r"""
        Bot has started successfully!
        """)
    print("\033[97m" + f'Logged in as {bot.user.name}')
    print(f'Connected to {len(bot.guilds)} guild(s).')

async def main():
    async with bot:
        await setup_extensions()
        await bot.start(TOKEN)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\r\nBot is shutting down...")

