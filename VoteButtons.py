import discord
from typing import Final
import datetime
import time
import asyncio
from Main import playAudio, active_votes

VOTE_SUCCESS_PATH: Final[str] = "sounds/voteSuccess.wav"
VOTE_YES_PATH: Final[str] = "sounds/voteYes.wav"
VOTE_FAIL_PATH: Final[str] = "sounds/voteFail.wav"
VOTE_NO_PATH: Final[str] = "sounds/voteNo.wav"

class VoteButtons(discord.ui.View):
    def __init__(self, target_user: discord.Member, vote_type: str, vc: discord.VoiceClient, interaction: discord.Interaction):
        super().__init__(timeout=20)  # 20-second timeout
        self.target_user = target_user
        self.yes_votes = 0
        self.no_votes = 0
        self.vote_type = vote_type
        self.vc = vc
        self.interaction = interaction
        self.people_voted = set()  # Track voters to prevent duplicate votes

    async def on_timeout(self):
        """Handle when the vote times out"""
        await self.finalize_vote()

    async def finalize_vote(self):
        """Process the final vote results"""
        # Disable all buttons
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
        
        # Determine outcome
        if self.check_winner():
            action_result = await self.execute_vote_action()
            await self.message.channel.send(
                f"Vote passed! {self.target_user.display_name} will be {action_result}."
            )
            await playAudio(VOTE_SUCCESS_PATH, self.vc, self.interaction)
        else:
            await self.message.channel.send(
                f"Vote failed. {self.target_user.display_name} will not be {self.vote_type}."
            )
            await playAudio(VOTE_FAIL_PATH, self.vc, self.interaction)
        
        # Clean up
        await asyncio.sleep(7)
        if self.vc.is_connected():
            await self.vc.disconnect()
        if self.interaction.guild.id in active_votes:
            active_votes.remove(self.interaction.guild.id)

    async def execute_vote_action(self) -> str:
        """Execute the appropriate action based on vote type"""
        try:
            match self.vote_type:
                case "timeout":
                    duration = datetime.timedelta(minutes=60)
                    await self.target_user.timeout(duration, reason="Voted timeout")
                    return "timed out"
                case "kick":
                    await self.target_user.kick(reason="Voted kick")
                    return "kicked"
                case "ban":
                    await self.target_user.ban(reason="Voted ban")
                    return "banned"
                case "mute":
                    await self.target_user.edit(mute=True)
                    return "muted"
                case "deafen":
                    await self.target_user.edit(deafen=True)
                    return "deafened"
                case "unmute":
                    await self.target_user.edit(mute=False)
                    return "unmuted"
                case "undeafen":
                    await self.target_user.edit(deafen=False)
                    return "undeafened"
                case _:
                    raise ValueError("Invalid vote type")
        except discord.Forbidden:
            await self.message.channel.send("I don't have permission to perform this action!")
            return "not affected (missing permissions)"
        except Exception as e:
            print(f"Error executing vote action: {e}")
            return "not affected (error occurred)"

    def check_winner(self) -> bool:
        """Determine if vote passed (60% threshold)"""
        total_votes = self.yes_votes + self.no_votes
        if total_votes == 0:
            return False
        return (self.yes_votes / total_votes) >= 0.6

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle yes votes"""
        if interaction.user.id in self.people_voted:
            await interaction.response.send_message("You've already voted!", ephemeral=True)
            return
            
        self.people_voted.add(interaction.user.id)
        self.yes_votes += 1
        await playAudio(VOTE_YES_PATH, self.vc, interaction)
        await interaction.response.send_message("You voted YES!", ephemeral=True)
        await self.update_vote_message()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle no votes"""
        if interaction.user.id in self.people_voted:
            await interaction.response.send_message("You've already voted!", ephemeral=True)
            return
            
        self.people_voted.add(interaction.user.id)
        self.no_votes += 1
        await playAudio(VOTE_NO_PATH, self.vc, interaction)
        await interaction.response.send_message("You voted NO!", ephemeral=True)
        await self.update_vote_message()

    async def update_vote_message(self):
        """Update the vote message with current counts"""
        embed = discord.Embed(
            title=f"Vote to {self.vote_type} {self.target_user.display_name}",
            description=(
                f"**Current Votes:**\n"
                f"✅ Yes: {self.yes_votes}\n"
                f"❌ No: {self.no_votes}\n"
                f"⏳ Timeout: {int(self.timeout - (time.time() - self.start_time))}s remaining"
            ),
            color=discord.Color.orange()
        )
        await self.message.edit(embed=embed)