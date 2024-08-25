import discord
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_name = '📁-log-moderation'

    def get_log_channel(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.name == self.log_channel_name:
                    return channel
        return None

    async def write_log(self, message: str):
        log_channel = self.get_log_channel()
        if log_channel:
            await log_channel.send(message)
        else:
            print(f"Channel '{self.log_channel_name}' not found.")

    @commands.Cog.listener()
    async def on_ready(self):
        log_channel = self.get_log_channel()
        if log_channel:
            await log_channel.send("Bot is ready!")
        else:
            print(f"Channel '{self.log_channel_name}' not found.")


async def setup(bot):
    await bot.add_cog(Logging(bot))

