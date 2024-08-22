import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

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


# Load the cogs
@bot.event
async def on_ready():
    await bot.load_extension('cogs.moderation')
    await bot.load_extension('cogs.reactions')
    await bot.load_extension('cogs.spam')
    print(f'Logged in as {bot.user.name}')


bot.run(TOKEN)
