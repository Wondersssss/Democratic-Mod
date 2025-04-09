# TOKEN ----------------
from typing import Final
import os
from dotenv import load_dotenv
# ======================

# DISCORD ---------------
import discord
from discord import Client, Intents, Message, app_commands
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

# BUTTON ESTABLISHING
class view(View):
    def __init__(self):
        print("Initialising buttons...")
        # Yes button
        self.add_item(Button(style=discord.ButtonStyle.green, label="Yes", emoji="✅", custom_id="yes"))

        # No button
        self.add_item(Button(style=discord.ButtonStyle.red, label="No", emoji="⛔", custom_id="no"))
        
        print("Buttons initialised!")


    # Called whenever a button is pressed
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.data["custom_id"] == "yes":
            print("Yes button clicked")
            await interaction.response.send_message("You pressed yes!", ephemeral=True)
            return "YES"
        
        else:
            print("No button clicked")
            await interaction.response.send_message("You clicked no!", ephemeral=True)
            return "NO"

            







# ------ TIMEOUT VOTE COMMAND ------

@client.tree.command(name="Vote Timeout", description="Vote to kick someone out the server", pass_context=True)
@app_commands.describe(user="The user to timeout")
@app_commands.checks.has_permissions(administrator=True)

async def voteTimeOut(interaction: discord.Interaction, userTarget: discord.User):
    if (interaction.user.voice):
        # Connects to the vc
        try:
            # FIXME: MAKE A SEPERATE FUNCTION FOR JOINING VC
            print(f"Attempting to join {interaction.message.author.voice.channel}")
            channel = interaction.message.author.voice.channel
            vc = await channel.connect(self_deaf=True)
            print(f"Joined {interaction.message.author.voice.channel}")

            audio = discord.FFmpegAudio(VOTE_START_PATH)
            vc.play(audio, after=lambda e: print(f"Player error: {e}"))

        except discord.errors.ClientException:
            print(f"Couldn't join voice channel {interaction.message.author.voice.channel}")
            await interaction.channel.send("Couldn't join the voice channel.")

        





    else:
        await interaction.channel.send("You aren't in a voice channel! Join one to invoke this.", ephemeral=True)

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



