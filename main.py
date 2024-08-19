import asyncio
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Synchroniser les commandes d'application avec le bot
@bot.event
async def on_ready():
    await bot.tree.sync()  # Synchronise les commandes
    print(f'Bot connecté en tant que {bot.user}!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
    else:
        raise error

# Commande traditionnelle
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author}!')

# Commande slash
@bot.tree.command(name="test", description="a test")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("This is a test!")

spam = True
created_channels = []  # Liste pour garder une trace des salons créés

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
        channel = await guild.create_text_channel(channel_name, category=category)
        created_channels.append(channel)  # Ajouter le salon à la liste des salons créés
        return channel
    return existing_channel

# Commande traditionnelle pour spammer un utilisateur
@bot.command()
@commands.has_role("Admin")
async def spam(ctx, member: discord.Member):
    global spam
    spam = True
    count = 0
    channel_count = 1

    category_name = "Spam Channels"  # Nom de la catégorie initiale
    category = await create_or_get_category(ctx.guild, category_name)

    while spam:
        if count >= 4:  # Si 5 messages sont envoyés, créer un nouveau salon
            count = 0
            channel_count += 1

            # Vérification du nombre de salons dans la catégorie
            if len(category.channels) >= 50:
                # Créer une nouvelle catégorie avec un nom unique
                category_name = f"Spam Channels {channel_count // 50 + 1}"
                category = await ctx.guild.create_category(category_name)

            channel_name = f'spam-channel-{channel_count}'
            channel = await create_channel(ctx, channel_name, category)
            ctx = await bot.get_context(await channel.send(f'Nouveau salon créé : {channel_name}'))

        await ctx.send(member.mention)
        count += 1
        await asyncio.sleep(0.1)

@bot.command()
@commands.has_role("Admin")
async def stop(ctx):
    global spam
    spam = False
    await ctx.send('Stopped!')

# Commande pour supprimer les salons créés par le bot
@bot.command()
@commands.has_role("Admin")
async def deleteSpam(ctx):
    global created_channels
    await ctx.send('Deleting spam channels in progress...')
    for channel in created_channels:
        await channel.delete()  # Supprimer chaque salon dans la liste
    created_channels = []  # Réinitialiser la liste après suppression
    await ctx.send('All spam channels have been deleted!')

@bot.command
async def howAreYou(ctx, member: discord.Member):
    await ctx.send(f'Im fine !! What about you {ctx.author.mention} ?')


token = os.getenv('BOT_TOKEN')
bot.run(token)
