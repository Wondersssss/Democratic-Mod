# TOKEN ----------------
from typing import Final
import os
from dotenv import load_dotenv
# ======================

# DISCORD ---------------
import discord
from discord import Client, Intents, app_commands
from discord.ui import Button, View
#========================

# GET TOKEN
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(f"Bot token: {TOKEN}")

# BOT SETUP
intents: Intents = Intents.all() # There's far too many specific intents to be enabled so admin
client: Client = Client(intents=intents)
print("Bot clients initialised")

# AUDIO FILES
VOTE_FAIL_PATH = "sounds/voteFail.wav"
VOTE_NO_PATH = "sounds/voteNo.wav"
VOTE_START_PATH = "sounds/voteStart.wav"
VOTE_SUCCESS_PATH = "sounds/voteSuccess.wav"
VOTE_YES_PATH = "sounds/voteYes.wav"

# Global vote tracking (consider using a database for persistence)
active_votes = {}  # Format: {message_id: {"yes": int, "no": int, "target": discord.User}}

class VoteButtons(discord.ui.View):
    def __init__(self, target_user: discord.User):
        super().__init__(timeout=30)  # 30-second timeout for the vote
        self.target_user = target_user
        self.yes_votes = 0
        self.no_votes = 0

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.yes_votes += 1
        await interaction.response.send_message("You voted YES" , ephemeral=True)
        await self.update_vote_message(interaction)

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.no_votes += 1
        await interaction.response.send_message("You voted NO", ephemeral=True)
        await self.update_vote_message(interaction)

    async def update_vote_message(self, interaction: discord.Interaction):
        # Edit the original vote message to show current counts
        embed = discord.Embed(
            title=f"Vote to timeout {self.target_user.display_name}",
            description=f"**Current Votes:**\n✅ Yes: {self.yes_votes}\n❌ No: {self.no_votes}",
            color=discord.Color.orange()
        )
        await interaction.message.edit(embed=embed)

    async def on_timeout(self):
        # Disable buttons when vote ends
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
        
        # Determine outcome
        channel = self.message.channel
        if self.yes_votes > self.no_votes:
            await channel.send(f"Vote passed! {self.target_user.display_name} will be timed out.")
            # Add your timeout logic here
        else:
            await channel.send(f"Vote failed. {self.target_user.display_name} will not be timed out.")

async def initiateVote(interaction: discord.Interaction, type: str, userTarget: discord.User):
    if interaction.user.voice:
        try:
            # Voice channel connection logic
            channel = interaction.message.author.voice.channel
            vc = await channel.connect(self_deaf=True)
            audio = discord.FFmpegAudio(VOTE_START_PATH)
            vc.play(audio, after=lambda e: print(f"Player error: {e}"))

            # Create and send vote message
            view = VoteButtons(userTarget)
            vote_message = await interaction.channel.send(
                f"Should we {type} {userTarget.mention}?",
                view=view
            )
            view.message = vote_message  # Store message reference
            
            return True
        except discord.errors.ClientException:
            await interaction.response.send_message("Couldn't join the voice channel.", ephemeral=True)
    else:
        await interaction.response.send_message("You're not in a VC!", ephemeral=True)
        return False

@client.tree.command(name="vote_timeout", description="Vote to timeout someone")
@app_commands.describe(user="The user to timeout")
@app_commands.checks.has_permissions(administrator=True)
async def voteTimeout(interaction: discord.Interaction, user: discord.User):
    await interaction.response.defer()
    await initiateVote(interaction, "time out", user)




    

# ---------------------------

# COMMAND SYNC
@client.event
async def on_ready():
    print(f"{client.user.name} is now online!")
    
    print("Syncing commands...")
    try:
        synced = await client.tree.sync()
        print(f"All {len(synced)} commands successfully synced!")
    except Exception as e:
        print(f"Command syncing unsuccessful: {e}")



