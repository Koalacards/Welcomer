import json
from typing import Optional

import discord


def create_embed(title, description, colour):
    embed = discord.Embed(title=title, description=description, colour=colour)
    return embed


def get_role_ids_from_str(role_ids: str):
    role_list = json.loads(role_ids)
    return role_list


async def send(
    interaction: discord.Interaction,
    embed: discord.Embed,
    view: Optional[discord.ui.View] = None,
    ephemeral: bool = False,
):
    if view:
        await interaction.response.send_message(
            embed=embed, view=view, ephemeral=ephemeral
        )
    else:
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
