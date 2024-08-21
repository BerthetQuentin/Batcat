from discord.ext import commands
import discord
import asyncio
from discord import Member

spam = True
created_channels = []


class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Static method to create or get a category in a guild
    @staticmethod
    async def create_or_get_category(guild, category_name):
        category = discord.utils.get(guild.categories, name=category_name)
        if not category:
            # Create the category if it does not exist
            category = await guild.create_category(category_name)
        return category

    # Static method to create a channel in a category or get it if it already exists
    @staticmethod
    async def create_channel(ctx, channel_name, category):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            # Create a new channel if it does not exist
            channel = await guild.create_text_channel(channel_name, category=category)
            created_channels.append(channel)
            return channel
        return existing_channel

    # Command to spam a member with messages in newly created channels
    @commands.command()
    @commands.has_role("Admin")
    async def spam(self, ctx, member: discord.Member = None):
        # Check if user has been selected
        if member is None:
            await ctx.send('Please specify a member to spam.')
            return

        global spam
        spam = True
        count = 0
        channel_count = 1

        category_name = "Spam Channels"  # Initial category name
        category = await self.create_or_get_category(ctx.guild, category_name)

        await ctx.send("Spam in progress...")
        await ctx.send("Use **+stop** for stopping the spam")

        while spam:
            if count >= 4:  # Create a new channel after 4 messages
                count = 0
                channel_count += 1

                # Check the number of channels in the category
                if len(category.channels) >= 50:
                    # Create a new category with a unique name
                    category_name = f"Spam Channels {channel_count // 50 + 1}"
                    category = await ctx.guild.create_category(category_name)

                channel_name = f'spam-channel-{channel_count}'
                channel = await self.create_channel(ctx, channel_name, category)
                await channel.send(f'New channel created: {channel_name}')

            # Send spam messages in all created channels
            for channel in created_channels:
                await channel.send(member.mention)
            count += 1
            await asyncio.sleep(0.1)

    # Command to stop spamming
    @commands.command()
    @commands.has_role("Admin")
    async def stop(self, ctx):
        global spam
        spam = False
        await ctx.send('Stopped!')
        await ctx.send("Use **+delete** for deleting the spam messages")

    # Command to delete all created spam channels and their categories
    @commands.command()
    @commands.has_role("Admin")
    async def delete(self, ctx):
        global created_channels, spam

        if spam:
            await ctx.send('Use **+stop** for stopping the spam before deleting the channels')
            return
        
        await ctx.send('Deleting spam channels in progress...')

        # Track categories to delete
        categories_to_delete = set()

        # Delete created channels
        for channel in created_channels:
            # Find the category of the channel
            category = channel.category
            await channel.delete()
            if category and len(category.channels) == 0:
                categories_to_delete.add(category)
        created_channels = []

        # Delete empty categories
        for category in categories_to_delete:
            await category.delete()

        await ctx.send('All spam channels and categories have been deleted!')


async def setup(bot):
    await bot.add_cog(Spam(bot))
