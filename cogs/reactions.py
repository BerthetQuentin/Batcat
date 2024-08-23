from discord.ext import commands

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages sent by the bot itself
        if message.author == self.bot.user:
            return

        # Check if the message starts with a command prefix
        if message.content.startswith('+'):
            return

        # Respond to "hello" in the message
        if 'hello' in message.content.lower():
            await message.channel.send(f'Hello {message.author.mention}!')

        # Respond to "bye" in the message
        if 'bye' in message.content.lower():
            await message.channel.send(f'Bye {message.author.mention}!')

async def setup(bot):
    await bot.add_cog(Reactions(bot))
