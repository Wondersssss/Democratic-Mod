from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents
from discord.ext import commands
import VoteButtons
import asyncio
import AudioPlayer

# Constants
CONNECTION_TIMEOUT = 30  # seconds
MAX_RETRIES = 2

# GET TOKEN
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(f"Bot token: {TOKEN}")

active_votes = []

# BOT SETUP
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

print("Bot intents initialized!")

VOTE_START_PATH: Final[str] = "sounds/voteStart.wav"

async def initiateVote(interaction: discord.Interaction, type: str, userTarget: discord.Member):
    if interaction.guild_id in active_votes:
        await interaction.followup.send("There's already an active vote in this server!", ephemeral=True)
        print(f"Vote cancelled due to one ongoing in {interaction.guild.name}.")
        return
    
    active_votes.append(interaction.guild.id)

    if not interaction.user.voice:
        await interaction.followup.send("You're not in a VC!", ephemeral=True)
        print("ERROR: User who invoked command is not in a VC")
        active_votes.remove(interaction.guild.id)
        return

    vc = None
    try:
        # Initialize voice client with retry logic
        for attempt in range(MAX_RETRIES):
            try:
                vc = await asyncio.wait_for(
                    interaction.user.voice.channel.connect(self_deaf=True),
                    timeout=CONNECTION_TIMEOUT
                )
                print(f"Connected to {interaction.user.voice.channel}!")
                break
            except asyncio.TimeoutError:
                if attempt == MAX_RETRIES - 1:
                    raise
                print(f"Connection timeout, retrying... ({attempt + 1}/{MAX_RETRIES})")
                await asyncio.sleep(1)
        
        # Play audio
        await AudioPlayer.playAudio(VOTE_START_PATH, vc, interaction)
        
        # Create vote
        view = VoteButtons.VoteButtons(userTarget, type, vc, interaction)
        vote_message = await interaction.channel.send(view=view)
        view.message = vote_message
        
    except asyncio.TimeoutError:
        await interaction.followup.send("Connection to voice channel timed out after multiple attempts.", ephemeral=True)
        print("ERROR: Voice connection timed out")
    except discord.ClientException as e:
        await interaction.followup.send(f"Voice connection error: {str(e)}", ephemeral=True)
        print(f"ERROR: Voice connection failed - {str(e)}")
    except Exception as e:
        await interaction.followup.send(f"An unexpected error occurred: {type(e).__name__}", ephemeral=True)
        print(f"ERROR: Unexpected error in initiateVote - {type(e).__name__}: {str(e)}")
    finally:
        if interaction.guild_id in active_votes:
            active_votes.remove(interaction.guild.id)
        if vc and vc.is_connected():
            await vc.disconnect()

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                await client.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")

@client.event
async def on_ready():
    print(f"{client.user.name} is now online!")
    print("Syncing commands...")
    await load_extensions()
    
    try:        
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")

if __name__ == '__main__':
    client.run(TOKEN)