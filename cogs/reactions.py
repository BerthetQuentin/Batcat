from discord.ext import commands


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Listen for specific message
        @commands.Cog.listener()
        async def on_message(self, message):
            if message.author == self.bot.user:
                return

            if 'hello' in message.content.lower():
                await message.channel.send(f'Hello {message.author} !')

            if 'bye' in message.content.lower():
                await message.channel.send(f'Bye {message.author} !')


async def setup(bot):
    await bot.add_cog(Reactions(bot))
