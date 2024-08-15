import asyncio
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Synchroniser les commandes d'application avec le bot
@bot.event
async def on_ready():
    await bot.tree.sync()  # Synchronise les commandes
    print(f'Bot connecté en tant que {bot.user}!')

# Commande traditionnelle
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author}!')

# Commande slash
@bot.tree.command(name="test", description="a test")
async def test(interaction: discord.Interaction):
        await interaction.response.send_message("This is a test!")

spam = True
# Commande traditionnelle
@bot.command()
async def spam(ctx, member: discord.Member):
    global spam
    spam = True
    while spam:
        await ctx.send(member.mention)
        await asyncio.sleep(0.1)

@bot.command()
async def stop(ctx):
    global spam
    spam = False
    await ctx.send('Stopped!')

token = os.getenv('BOT_TOKEN')
bot.run(token)
