# TOKEN ----------------
from typing import Final
import os
from dotenv import load_dotenv
# ======================

# DISCORD ---------------
import discord
from discord import Client, Intents, app_commands
#========================

# OTHER FILES -----------
from VoteButtons import *
#========================

# GET TOKEN
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(f"Bot token: {TOKEN}")

# BOT SETUP
intents: Intents = Intents.all() # There's far too many specific intents to be enabled so admin
client: Client = Client(intents=intents)
print("Bot clients initialised")

VOTE_START_PATH: Final[str] = "sounds/voteStart.wav"

async def initiateVote(interaction: discord.Interaction, type: str, userTarget: discord.Member):
    if interaction.user.voice:
        try:
            # Voice channel connection logic
            channel = interaction.message.author.voice.channel
            print(f"Attempting to join {channel.name}...")
            vc = await channel.connect(self_deaf=True)
            print(f"Joined {channel.name}, playing the vote start sound...")
            audio = discord.FFmpegAudio(VOTE_START_PATH)
            vc.play(audio, after=lambda e: print(f"Player error: {e}"))
            print("Bot has successfully played vote start audio!")

            # Create and send vote message
            view = VoteButtons(userTarget, type, vc, interaction)
            vote_message = await interaction.channel.send(view=view)
            view.message = vote_message  # Store message reference
        except discord.errors.ClientException:
            await interaction.response.send_message("Couldn't join the voice channel.", ephemeral=True)
            print("ERROR: Bot was unable to join vc")
    else:
        await interaction.response.send_message("You're not in a VC!", ephemeral=True)
        print("ERROR: User who invoked command is not in a VC")


async def playAudio(file, vc: discord.VoiceClient, interaction: discord.Interaction):
    if interaction.user.voice and vc.is_connected:
        print(f"Attempting to play {file}...")
        vc.play(file, after=lambda e: print(f"Player error: {e}"))
        print(f"{file} played!")
    else:
        print("ERROR: Bot or command caller isn't in VC")
        await interaction.response.send_message("Bot or command caller isn't in VC!")



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



