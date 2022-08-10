import discord
from discord.ext import commands
from discord import app_commands
from confidential import RUN_ID
import dbfunc
import json

class Welcomer(commands.Bot):
    def __init__(self, *, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
    
    async def on_ready(self):
        print("ready")
        await self.tree.sync()
    
    async def on_member_join(self, member):
        print("member joined")
        guild = member.guild
        welcome_channel_id = dbfunc.get_channel_id(guild.id)
        welcome_message = dbfunc.get_welcome_message(guild.id)
        #Welcome channel has not been set (or just guild settings in general)
        if welcome_channel_id == 0 or welcome_channel_id is None:
            return
        
        welcome_channel = welcomer.get_channel(welcome_channel_id)
        await welcome_channel.send(f"{member.mention}: {welcome_message}")

        role_ids = _get_role_ids_from_str(dbfunc.get_role_ids(guild.id))

        for role_id in role_ids:
            welcome_role = guild.get_role(role_id)
            await member.add_roles(welcome_role)


intents = discord.Intents.default()
intents.members = True

welcomer = Welcomer(command_prefix=".", intents=intents)

def _create_embed(title, description, colour):
    embed = discord.Embed(title=title, description=description, colour=colour)
    return embed

def _get_role_ids_from_str(role_ids:str):
    role_list = json.loads(role_ids)
    return role_list


@welcomer.tree.command(name='set_welcome_channel')
async def set_welcome_channel(interaction: discord.Interaction, channel:discord.TextChannel):
    """Set the welcome channel to welcome people to the discord"""
    author = interaction.user
    if author.guild_permissions.administrator == True or author.guild_permissions.manage_guild == True:
        guild_id = interaction.guild_id
        dbfunc.set_channel_id(guild_id, channel.id)
        
        title="Success"
        description="Welcome channel set successfully!"
        colour=discord.Color.green()
        await interaction.response.send_message(embed=_create_embed(title, description, colour))
    else:
        title="Error"
        description="You must have `ADMINISTRATOR` or `MANAGE_GUILD` permissions to run this command."
        colour=discord.Color.red()

        await interaction.response.send_message(embed=_create_embed(title, description, colour))

@welcomer.tree.command(name='add_welcome_role')
async def add_welcome_role(interaction: discord.Interaction, role:discord.Role):
    """Add a role to welcome the users with"""
    author = interaction.user
    if author.guild_permissions.administrator == True or author.guild_permissions.manage_guild == True:
        guild_id = interaction.guild_id
        role_id = role.id
        role_ids = _get_role_ids_from_str(dbfunc.get_role_ids(guild_id))

        if role_id not in role_ids:
            role_ids.append(role_id)
            dbfunc.set_role_ids(guild_id, str(role_ids))

            title="Success"
            description="Welcome role added successfully!"
            colour=discord.Color.green()
            await interaction.response.send_message(embed=_create_embed(title, description, colour))
        
        else:
            title="Error"
            description="The role you wanted to add is already in your list of welcome roles!"
            colour=discord.Color.red()
            await interaction.response.send_message(embed=_create_embed(title, description, colour))
        
    else:
        title="Error"
        description="You must have `ADMINISTRATOR` or `MANAGE_GUILD` permissions to run this command."
        colour=discord.Color.red()

        await interaction.response.send_message(embed=_create_embed(title, description, colour))

@welcomer.tree.command(name='remove_welcome_role')
async def remove_welcome_role(interaction: discord.Interaction, role:discord.Role):
    """Remove a role to welcome users with"""
    author = interaction.user
    if author.guild_permissions.administrator == True or author.guild_permissions.manage_guild == True:
        guild_id = interaction.guild_id
        role_id = role.id
        role_ids = _get_role_ids_from_str(dbfunc.get_role_ids(guild_id))

        if role_id not in role_ids:
            title="Error"
            description="The role you wanted to remove is not in your list of welcome roles!"
            colour=discord.Color.red()
            await interaction.response.send_message(embed=_create_embed(title, description, colour))

        else:
            role_ids.remove(role_id)
            dbfunc.set_role_ids(guild_id, str(role_ids))

            title="Success"
            description="Welcome role removed successfully!"
            colour=discord.Color.green()
            await interaction.response.send_message(embed=_create_embed(title, description, colour))
    else:
        title="Error"
        description="You must have `ADMINISTRATOR` or `MANAGE_GUILD` permissions to run this command."
        colour=discord.Color.red()

        await interaction.response.send_message(embed=_create_embed(title, description, colour))

@welcomer.tree.command(name='set_welcome_message')
async def set_welcome_message(interaction: discord.Interaction, welcome_message:str):
    """Set the welcome message for the server"""
    author = interaction.user
    if author.guild_permissions.administrator == True or author.guild_permissions.manage_guild == True:
        guild_id = interaction.guild_id
        dbfunc.set_welcome_message(guild_id, welcome_message)
        
        title="Success"
        description="Welcome message set successfully!"
        colour=discord.Color.green()
        await interaction.response.send_message(embed=_create_embed(title, description, colour))
    else:
        title="Error"
        description="You must have `ADMINISTRATOR` or `MANAGE_GUILD` permissions to run this command."
        colour=discord.Color.red()

        await interaction.response.send_message(embed=_create_embed(title, description, colour))



welcomer.run(RUN_ID)