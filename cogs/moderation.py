import asyncio
import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions
from utils.role_manager import assign_role, remove_role


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to kick
    @commands.command(name='kick')
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked for: {reason}')
        print(f'{member.mention} has been kicked for: {reason}')

    # Command to ban
    @commands.command(name='ban')
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned for: {reason}')
        print(f'{member.mention} has been banned for: {reason}')

    # Command to unban
    @commands.command(name='unban')
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        if member.isdigit():
            member_id = int(member)
        else:
            member_id = None

        async for ban_entry in ctx.guild.bans():
            user = ban_entry.user
            if user.id == member_id or f"{user.name}#{user.discriminator}" == member:
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} has been unbanned from the server')
                print(f'{user.mention} has been unbanned from the server')
                return

        # if no user's found
        await ctx.send(f'User {member} not found')
        print(f'{member} not found')

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
                                              read_messages=True)

        await member.add_roles(role, reason=reason)
        await ctx.send(f'{member.mention} has been muted for {minutes} minutes for: {reason}')
        print(f'{member.name} has been muted for {minutes} minutes for: {reason}')

        if minutes > 0:
            await asyncio.sleep(minutes * 60)
            await member.remove_roles(role)
            await ctx.send(f'{member.mention} has served his sentence')
            print(f'{member.name} has been unmuted')

    # Command to unmute
    @commands.command(name='unmute')
    @has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: Member):
        role = discord.utils.get(ctx.guild.roles, name='muted')
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f'{member.name} has been unmuted by {ctx.author}')
            print(f'{member.name} has been unmuted by {ctx.author}')
        else:
            await ctx.send(f'{member.name} is not muted')
            print(f'{member.name} has been unmuted')

    # When new member join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role_name = "membre"
        success = await assign_role(member, role_name)
        if success:
            print(f"The role '{role_name}' has been assigned to {member.name}.")
        else:
            print(f"The role '{role_name}' was not found for {member.name}.")

    # add roles
    @commands.command(name='add')
    async def add(self, ctx, member: Member, role_name=None):
        logging_cog = self.bot.get_cog('Logging')
        success = await assign_role(member, role_name)

        if success:
            await ctx.send(f'{member.mention} has been added to {role_name}')
            print(f"The role '{role_name}' has been assigned to {member.name}.")
            if logging_cog:
                await logging_cog.write_log(f"The role '{role_name}' has been assigned to {member.name}.")
        else:
            await ctx.send(f'{member.mention} was not added to {role_name}')
            print(f"The role '{role_name}' was not added for {member.name}.")

    # Remove roles
    @commands.command(name='remove')
    async def remove(self, ctx, member: Member, role_name=None):
        logging_cog = self.bot.get_cog('Logging')
        success = await remove_role(member, role_name)

        if success:
            await ctx.send(f'{member.mention} has been removed from {role_name}')
            print(f"The role '{role_name}' has been removed from {member.name}.")
            if logging_cog:
                await logging_cog.write_log(f"The role '{role_name}' has been removed from {member.name}.")
        else:
            await ctx.send(f'{member.mention} was not removed from {role_name}')
            print(f"The role '{role_name}' was not removed for {member.name}.")
            if logging_cog:
                await logging_cog.write_log(f"The role '{role_name}' was not removed for {member.name}.")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
