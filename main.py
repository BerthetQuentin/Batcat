import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author}')


token = os.getenv('BOT_TOKEN')
bot.run(token)
