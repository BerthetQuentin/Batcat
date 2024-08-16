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

# Fonction pour créer une catégorie ou obtenir une catégorie existante
async def create_or_get_category(guild, category_name):
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        category = await guild.create_category(category_name)
    return category

# Fonction pour créer un nouveau salon dans une catégorie
async def create_channel(ctx, channel_name, category):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        return await guild.create_text_channel(channel_name, category=category)
    return existing_channel

# Commande traditionnelle pour spammer un utilisateur
@bot.command()
async def spam(ctx, member: discord.Member):
    global spam
    spam = True
    count = 0
    channel_count = 1

    category_name = "Spam Channels"  # Nom de la catégorie
    category = await create_or_get_category(ctx.guild, category_name)

    while spam:
        if count >= 5:  # Si 5 messages sont envoyés, créer un nouveau salon
            count = 0
            channel_count += 1
            channel_name = f'spam-{member}-{channel_count}'
            channel = await create_channel(ctx, channel_name, category)
            ctx = await bot.get_context(await channel.send(f'Nouveau salon créé : {channel_name}'))

        await ctx.send(member.mention)
        count += 1
        await asyncio.sleep(0.1)

@bot.command()
async def stop(ctx):
    global spam
    spam = False
    await ctx.send('Stopped!')

token = os.getenv('BOT_TOKEN')
bot.run(token)
