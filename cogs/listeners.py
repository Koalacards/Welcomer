import discord
from discord.ext import commands

import data.dbfunc as dbfunc
from utils import get_role_ids_from_str


class Listeners(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        print("member joined")
        guild = member.guild
        welcome_channel_id = dbfunc.get_channel_id(guild.id)
        welcome_message = dbfunc.get_welcome_message(guild.id)
        # If welcome channel or welcome message has not been set, this wont work
        if (
            welcome_channel_id == 0
            or welcome_channel_id is None
            or welcome_message == ""
        ):
            return

        welcome_channel = self.client.get_channel(welcome_channel_id)
        await welcome_channel.send(f"**{member.display_name}**: {welcome_message}")

        role_ids = get_role_ids_from_str(dbfunc.get_role_ids(guild.id))

        for role_id in role_ids:
            welcome_role = guild.get_role(role_id)
            await member.add_roles(welcome_role)


async def setup(client: commands.Bot):
    await client.add_cog(Listeners(client))
