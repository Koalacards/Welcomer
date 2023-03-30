import discord
from discord.ext import commands, tasks
from confidential import RUN_ID

class Welcomer(commands.Bot):
    def __init__(self, *, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
    
    async def on_ready(self):
        print("ready")
        self.update_presence.start()

    async def setup_hook(self) -> None:
        await client.load_extension('cogs.setup_commands')
        await client.load_extension('cogs.listeners')
        await client.load_extension('cogs.utility_commands')
        await self.tree.sync()

    @tasks.loop(minutes=30)
    async def update_presence(self):
        guild_count = str(len(client.guilds))
        await client.change_presence(
            activity=discord.Game(name=f"Welcoming users in {guild_count} servers! /help for setup!")
        )


intents = discord.Intents.default()
intents.members = True

client = Welcomer(command_prefix="~~~", intents=intents)


client.run(RUN_ID)