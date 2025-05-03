import discord
from discord.ext import commands
from discord import app_commands

# All commands to test specific functions
class TestCommands(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name="test", description="Test command to verify bot functionality")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("Bot is working!", ephemeral=True)

async def setup(client):
    await client.add_cog(TestCommands(client))