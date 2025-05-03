# Main.py
from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Client, Intents, app_commands
from discord.ext import commands
from VoteButtons import VoteButtons

# Load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

class VoteBot(commands.Bot):
    def __init__(self):
        intents = Intents.default()
        intents.message_content = True
        intents.voice_states = True
        super().__init__(command_prefix='!', intents=intents)
        self.active_votes = []
        self.ADMIN_ONLY = True
        self.VOTE_START_PATH = "sounds/voteStart.wav"

    async def initiate_vote(self, interaction: discord.Interaction, vote_type: str, target_user: discord.Member):
        if interaction.guild_id in self.active_votes:
            await interaction.response.send_message("There's already an active vote in this server!", ephemeral=True)
            return False

        if not interaction.user.voice:
            await interaction.response.send_message("You must be in a voice channel to start a vote!", ephemeral=True)
            return False

        try:
            channel = interaction.user.voice.channel
            vc = await channel.connect(self_deaf=True)
            audio = discord.FFmpegPCMAudio(self.VOTE_START_PATH)
            vc.play(audio)
            
            view = VoteButtons(self, target_user, vote_type, vc, interaction)
            await interaction.response.send_message(f"Starting vote to {vote_type} {target_user.display_name}...")
            view.message = await interaction.original_response()
            self.active_votes.append(interaction.guild_id)
            return True
        except Exception as e:
            print(f"Error starting vote: {e}")
            await interaction.response.send_message("Failed to start vote", ephemeral=True)
            return False

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        await self.load_extension('cogs.vote_commands')
        await self.load_extension('cogs.test_commands')
        
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(f"Error syncing commands: {e}")

bot = VoteBot()

if __name__ == '__main__':
    bot.run(TOKEN)