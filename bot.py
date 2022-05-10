import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.cog_ext import manage_commands
from confidential import RUN_ID
import dbfunc
import json

#guild_ids = [876103457407385661]

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(".", intents=intents)
slash = SlashCommand(client, sync_commands=True, override_type=True)

def _create_embed(title, description, colour):
    embed = discord.Embed(title=title, description=description, colour=colour)
    return embed

def _get_role_ids_from_str(role_ids:str):
    role_list = json.loads(role_ids)
    return role_list

set_welcome_channel_options = [
    manage_commands.create_option(
        name='channel',
        description='The welcome channel',
        option_type= 7,
        required=True
    )
]
  
role_options = [
    manage_commands.create_option(
        name='role',
        description='The role',
        option_type=8,
        required=True
    )
]
@client.event
async def on_ready():
    print("ready")

@client.event
async def on_member_join(member):
    print("member joined")
    guild = member.guild
    welcome_channel_id = dbfunc.get_channel_id(guild.id)
    welcome_message = dbfunc.get_welcome_message(guild.id)
    #Welcome channel has not been set (or just guild settings in general)
    if welcome_channel_id == 0 or welcome_channel_id is None:
        return
    
    welcome_channel = client.get_channel(welcome_channel_id)
    await welcome_channel.send(f"{member.mention}: {welcome_message}")

    role_ids = _get_role_ids_from_str(dbfunc.get_role_ids(guild.id))

    for role_id in role_ids:
        welcome_role = guild.get_role(role_id)
        await member.add_roles(welcome_role)


@slash.slash(name='set_welcome_channel',
 #guild_ids=guild_ids,
 description='Set the welcome channel to welcome people to the discord', options=set_welcome_channel_options)
async def set_welcome_channel(ctx, channel:discord.TextChannel):
    author = ctx.author
    if author.guild_permissions.administrator == True or author.guild_permissions.manage_guild == True:
        guild_id = ctx.guild.id
        dbfunc.set_channel_id(guild_id, channel.id)
        
        title="Success"
        description="Welcome channel set successfully!"
        colour=discord.Color.green()
        await ctx.send(embed=_create_embed(title, description, colour))
    else:
        title="Error"
        description="You must have `ADMINISTRATOR` or `MANAGE_GUILD` permissions to run this command."
        colour=discord.Color.red()

        await ctx.send(embed=_create_embed(title, description, colour))

@slash.slash(name='add_welcome_role', 
#guild_ids=guild_ids, 
description='Add a role to welcome the users with', options=role_options)
async def add_welcome_role(ctx, role:discord.Role):
    author = ctx.author
    if author.guild_permissions.administrator == True or author.guild_permissions.manage_guild == True:
        guild_id = ctx.guild.id
        role_id = role.id
        role_ids = _get_role_ids_from_str(dbfunc.get_role_ids(guild_id))

        if role_id not in role_ids:
            role_ids.append(role_id)
            dbfunc.set_role_ids(guild_id, str(role_ids))

            title="Success"
            description="Welcome role added successfully!"
            colour=discord.Color.green()
            await ctx.send(embed=_create_embed(title, description, colour))
        
        else:
            title="Error"
            description="The role you wanted to add is already in your list of welcome roles!"
            colour=discord.Color.red()
            await ctx.send(embed=_create_embed(title, description, colour))
        
    else:
        title="Error"
        description="You must have `ADMINISTRATOR` or `MANAGE_GUILD` permissions to run this command."
        colour=discord.Color.red()

        await ctx.send(embed=_create_embed(title, description, colour))

@slash.slash(name='remove_welcome_role', 
#guild_ids=guild_ids, 
description='Remove a role to welcome users with', options=role_options)
async def remove_welcome_role(ctx, role:discord.Role):
    author = ctx.author
    if author.guild_permissions.administrator == True or author.guild_permissions.manage_guild == True:
        guild_id = ctx.guild.id
        role_id = role.id
        role_ids = _get_role_ids_from_str(dbfunc.get_role_ids(guild_id))

        if role_id not in role_ids:
            title="Error"
            description="The role you wanted to remove is not in your list of welcome roles!"
            colour=discord.Color.red()
            await ctx.send(embed=_create_embed(title, description, colour))

        else:
            role_ids.remove(role_id)
            dbfunc.set_role_ids(guild_id, str(role_ids))

            title="Success"
            description="Welcome role removed successfully!"
            colour=discord.Color.green()
            await ctx.send(embed=_create_embed(title, description, colour))
    else:
        title="Error"
        description="You must have `ADMINISTRATOR` or `MANAGE_GUILD` permissions to run this command."
        colour=discord.Color.red()

        await ctx.send(embed=_create_embed(title, description, colour))

@slash.slash(name='set_welcome_message', 
#guild_ids=guild_ids, 
description="Set the welcome message for the server")
async def set_welcome_message(ctx, welcome_message:str):
    author = ctx.author
    if author.guild_permissions.administrator == True or author.guild_permissions.manage_guild == True:
        guild_id = ctx.guild.id
        dbfunc.set_welcome_message(guild_id, welcome_message)
        
        title="Success"
        description="Welcome message set successfully!"
        colour=discord.Color.green()
        await ctx.send(embed=_create_embed(title, description, colour))
    else:
        title="Error"
        description="You must have `ADMINISTRATOR` or `MANAGE_GUILD` permissions to run this command."
        colour=discord.Color.red()

        await ctx.send(embed=_create_embed(title, description, colour))



client.run(RUN_ID)