import asyncio
import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to kick
    @commands.command(name='kick')
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked for: {reason}')

    # Command to ban
    @commands.command(name='ban')
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned for: {reason}')

    # Command to unban
    @commands.command(name='unban')
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name == member:
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} has been unbanned from the server')
                return
        await ctx.send(f'User {member} not found')

    # Command to mute
    @commands.command(name='mute')
    @has_permissions(manage_roles=True)
    async def mute(self, ctx, member: Member, minutes: int = 0, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name='muted')
        if not role:
            role = await ctx.guild.create_role(name="muted")

            for channel in ctx.guild.channels:
                await channel.set_permissions(role,
                                              speak=False,
                                              send_messages=False,
                                              read_message_history=True,
                                              read_messages=False)

        await member.add_roles(role, reason=reason)
        await ctx.send(f'{member.name} has been muted for {minutes} minutes for: {reason}')

        if minutes > 0:
            await asyncio.sleep(minutes * 60)
            await member.remove_roles(role)
            await ctx.send(f'{member.name} has been unmuted')

    @commands.command(name='unmute')
    @has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: Member):
        role = discord.utils.get(ctx.guild.roles, name='muted')
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f'{member.name} has been unmuted by {ctx.author}')
        else:
            await ctx.send(f'{member.name} is not muted')


async def setup(bot):
    await bot.add_cog(Moderation(bot))
