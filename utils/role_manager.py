import discord

# Function to assign a role to a member
async def assign_role(member, role_name):
    role = discord.utils.get(member.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        return True
    return False

# Function to remove a role to a member
async def remove_role(member, role_name):
    role = discord.utils.get(member.guild.roles, name=role_name)
    if role:
        await member.remove_roles(role)
        return True
    return False

# Function to check if member have role
async def check_role(member):
    roles = discord.utils.get(member.guild.roles)
    if roles:
        return roles
    else:
        return False

