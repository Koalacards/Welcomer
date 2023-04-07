import discord
from discord import app_commands
from discord.ext import commands

import data.dbfunc as dbfunc
from utils import create_embed, get_role_ids_from_str, send
from views import url_view


class SetupCommands(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="set-welcome-channel")
    @app_commands.describe(channel="Channel where Welcomer will greet new users!")
    @app_commands.default_permissions(manage_guild=True)
    async def set_welcome_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        """Set the channel where Welcomer will greet new users!"""
        guild_id = interaction.guild_id
        dbfunc.set_channel_id(guild_id, channel.id)

        title = "Success!"
        description = "Welcome channel set successfully!"
        colour = discord.Color.green()
        await send(
            interaction,
            embed=create_embed(title, description, colour),
            view=url_view,
            ephemeral=True,
        )

    @app_commands.command(name="add-welcome-role")
    @app_commands.describe(role="Role to welcome the users with!")
    @app_commands.default_permissions(manage_guild=True)
    async def add_welcome_role(
        self, interaction: discord.Interaction, role: discord.Role
    ):
        """Add a role to welcome the users with!"""
        guild_id = interaction.guild_id
        role_id = role.id
        role_ids = get_role_ids_from_str(dbfunc.get_role_ids(guild_id))

        if role_id not in role_ids:
            role_ids.append(role_id)
            dbfunc.set_role_ids(guild_id, str(role_ids))

            title = "Success!"
            description = "Welcome role added successfully!"
            colour = discord.Color.green()
            await send(
                interaction,
                embed=create_embed(title, description, colour),
                view=url_view,
                ephemeral=True,
            )

        else:
            title = "Error"
            description = (
                "The role you wanted to add is already in your list of welcome roles!"
            )
            colour = discord.Color.red()
            await send(
                interaction,
                embed=create_embed(title, description, colour),
                view=url_view,
                ephemeral=True,
            )

    @app_commands.command(name="remove-welcome-role")
    @app_commands.describe(role="Role you wish to remove from welcoming users with.")
    @app_commands.default_permissions(manage_guild=True)
    async def remove_welcome_role(
        self, interaction: discord.Interaction, role: discord.Role
    ):
        """Remove a role to welcome users with."""
        guild_id = interaction.guild_id
        role_id = role.id
        role_ids = get_role_ids_from_str(dbfunc.get_role_ids(guild_id))

        if role_id not in role_ids:
            title = "Error"
            description = (
                "The role you wanted to remove is not in your list of welcome roles!"
            )
            colour = discord.Color.red()
            await send(
                interaction,
                embed=create_embed(title, description, colour),
                view=url_view,
                ephemeral=True,
            )

        else:
            role_ids.remove(role_id)
            dbfunc.set_role_ids(guild_id, str(role_ids))

            title = "Success!"
            description = "Welcome role removed successfully!"
            colour = discord.Color.green()
            await send(
                interaction,
                embed=create_embed(title, description, colour),
                view=url_view,
                ephemeral=True,
            )

    @app_commands.command(name="set-welcome-message")
    @app_commands.describe(
        welcome_message="The message all users will get when they enter the server!"
    )
    @app_commands.default_permissions(manage_guild=True)
    async def set_welcome_message(
        self, interaction: discord.Interaction, welcome_message: str
    ):
        """Set the welcome message for the server!"""
        guild_id = interaction.guild_id
        dbfunc.set_welcome_message(guild_id, welcome_message)

        title = "Success!"
        description = "Welcome message set successfully!"
        colour = discord.Color.green()
        await send(
            interaction,
            embed=create_embed(title, description, colour),
            view=url_view,
            ephemeral=True,
        )


async def setup(client: commands.Bot):
    await client.add_cog(SetupCommands(client))
