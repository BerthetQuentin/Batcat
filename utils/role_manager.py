import discord

# Function to assign a role to a member
async def assign_role(member, role_name):
    role = discord.utils.get(member.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        return True
    return False
