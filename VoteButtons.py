import discord
from discord import Client, Intents, app_commands
from discord.ui import Button, View
from Main import *
from typing import Final
import datetime

VOTE_SUCCESS_PATH: Final[str] = "sounds/voteSuccess.wav"
VOTE_YES_PATH: Final[str] = "sounds/voteYes.wav"
VOTE_FAIL_PATH: Final[str] = "sounds/voteFail.wav"
VOTE_NO_PATH: Final[str] = "sounds/voteNo.wav"

# Global vote tracking 
active_votes = {}  # Format: {message_id: {"yes": int, "no": int, "target": discord.User}}

class VoteButtons(discord.ui.View):
    def __init__(self, target_user: discord.Member, type: str, vc: discord.VoiceClient, interaction: discord.Interaction):
        super().__init__(timeout=20)  # 30-second timeout for the vote
        self.target_user = target_user
        self.yes_votes = 0
        self.no_votes = 0
        self.type = type
        self.vc = vc
        self.interaction = interaction

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes_button(self, button: discord.ui.Button):
        playAudio(discord.FFmpegAudio(VOTE_YES_PATH), self.vc, self.interaction)
        self.yes_votes += 1
        await self.interaction.response.send_message("You voted YES!" , ephemeral=True)
        await self.update_vote_message(self.interaction)

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no_button(self, button: discord.ui.Button):
        playAudio(discord.FFmpegAudio(VOTE_NO_PATH), self.vc, self.interaction)
        self.no_votes += 1
        await self.interaction.response.send_message("You voted NO!", ephemeral=True)
        await self.update_vote_message(self.interaction)

    async def update_vote_message(self, interaction: discord.Interaction):
        # Edit the original vote message to show current counts
        embed = discord.Embed(
            title=f"Vote to {self.type} {self.target_user.display_name}?",
            description=f"**Current Votes:**\n✅ Yes: {self.yes_votes}\n❌ No: {self.no_votes}",
            color=discord.Color.orange()
        )
        await interaction.message.edit(embed=embed)

    async def voteAction(self):
        match self.type:
            case "timeout":
                await self.target_user.timeout(datetime.delta(seconds=30*60), reason="Voted out by the public")
                return "timed out"
            case "time out":
                await self.target_user.timeout(datetime.delta(seconds=30*60), reason="Voted out by the public")
                return "timed out"
            case "kick":
                self.target_user.kick(reason="Voted out by the public")
                return "kicked"
            case "ban":
                self.target_user.ban(reason="Voted out by the public")
                return "banned"
            case "mute":
                self.target_user.edit(mute=True)
                return "muted"
            case "deafen":
                self.target_user.edit(deafen=True)
                return "deafened"
            case "unmute":
                self.target_user.edit(mute=False)
                return "unmuted"
            case "undeafen":
                self.target_user.edit(deafen=False)
                return "undeafened"
            case _:
                self.interaction.response.send_message("Invalid type was sent, try using /Help", ephemeral=True)

    async def on_timeout(self):
        # Disable buttons when vote ends
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
        
        # Determine outcome
        channel = self.message.channel
        
        if self.yes_votes > self.no_votes:
            typeStr = self.voteAction(self)
            await channel.send(f"Vote passed! {self.target_user.display_name} will be {typeStr}.")
            playAudio(discord.FFmpegAudio(VOTE_YES_PATH), self.vc, self.interaction)
        else:
            await channel.send(f"Vote failed. {self.target_user.display_name} will not be {typeStr}.")
            playAudio(discord.FFmpegAudio(VOTE_NO_PATH), self.vc, self.interaction)

    
