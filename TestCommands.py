import discord
from discord import Client, Intents, app_commands
from Main import *

# All commands to test specific functions

@tree.command(name="test", description="Test command to verify bot functionality")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("Bot is working!", ephemeral=True)