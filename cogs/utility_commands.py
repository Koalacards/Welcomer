import discord
from discord import app_commands
from discord.ext import commands
from utils import send, create_embed
from views import url_view
from confidential import SUGGESTION_CHANNEL_ID


class UtilityCommands(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @app_commands.command(name="help")
    async def help(self, interaction:discord.Interaction):
        """Displays the commands to use Welcomer!"""
        title= "Welcomer Help Page"
        description= (
            "Thanks for adding Welcomer to your server! This is a simple bot that welcomes new users to your server and adds any roles you want to them!\n\n"
            "**Commands for all users**\n\n"
            "**suggest**: Make a suggestion or report a bug directly to the Welcomer devs!\n\n"
            "**help**: Displays this message.\n\n"
            "**Setup Commands (For Mods Only)**\n\n"
            "**set-welcome-channel**: Set the channel where Welcomer will welcome users! This has to be set for Welcomer to work.\n\n"
            "**set-welcome-message**: Set the message that Welcomer will greet users with! This has to be set for Welcomer to work.\n\n"
            "**add-welcome-role**: Add a role that Welcomer will automatically assign when users join!\n\n" 
            "**Make sure the \"Welcomer\" bot role is above the roles you want to add, or else there will be permission errors!**\n\n"
            "**remove-welcome-role**: Remove a role that Welcomer will automatically assign when users join!\n\n"
            "Happy welcoming!"
        )
        color=discord.Color.dark_orange()
        await send(
            interaction,
            create_embed(title, description, color),
            view=url_view
        )

    @app_commands.command(name="suggest")
    @app_commands.describe(suggestion="Something to suggest for the Welcomer devs!")
    async def suggest(self, interaction: discord.Interaction, suggestion: str) -> None:
        """Suggest an improvement or report a bug regarding the Welcomer bot!"""
        suggestion_channel = self.client.get_channel(SUGGESTION_CHANNEL_ID)
        await suggestion_channel.send(
            embed=create_embed(
                f"New Suggestion from {interaction.user.name}",
                suggestion,
                discord.Color.dark_orange()
            )
        )

        await send(
            interaction,
            create_embed(
                "Success!",
                "Your suggestion or report has been sent to the devs, thank you for supporting Welcomer!",
                discord.Color.green()
            ),
            view=url_view,
            ephemeral=True
        )


async def setup(client: commands.Bot):
    await client.add_cog(UtilityCommands(client))