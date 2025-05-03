from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents
from discord.ext import commands
import VoteButtons


# GET TOKEN
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(f"Bot token: {TOKEN}")

active_votes = []

# BOT SETUP
intents= discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

print("Bot intents initialised!")

VOTE_START_PATH: Final[str] = "sounds/voteStart.wav"

async def initiateVote(interaction: discord.Interaction, type: str, userTarget: discord.Member):
    if interaction.guild_id in active_votes:
        await interaction.followup.send("There's already an active vote in this server!", ephemeral=True)
        print(f"Vote cancelled due to one ongoing in {interaction.guild.name}.")
        return
    
    active_votes.append(interaction.guild.id)

    if interaction.user.voice:
        try:
            channel = interaction.user.voice.channel
            print(f"Attempting to join {channel.name}...")
            vc = await channel.connect(self_deaf=True)
            await playAudio(VOTE_START_PATH, vc, interaction)

            view = VoteButtons.VoteButtons(userTarget, type, vc, interaction)
            vote_message = await interaction.channel.send(view=view)
            view.message = vote_message
        except discord.errors.ClientException:
            await interaction.followup.send("Couldn't join the voice channel.", ephemeral=True)
            print("ERROR: Bot was unable to join vc")
    else:
        await interaction.followup.send("You're not in a VC!", ephemeral=True)
        print("ERROR: User who invoked command is not in a VC")

async def playAudio(file, vc: discord.VoiceClient, interaction: discord.Interaction):
    if vc.is_connected():
        print(f"Attempting to play {file}...")
        audio = discord.FFmpegPCMAudio(file)
        vc.play(audio, after=lambda e: print(f"Player error: {e}") if e else None)
        print(f"{file} played!")
    else:
        print("ERROR: Bot isn't in VC")
        await interaction.followup.send("Bot isn't in VC!", ephemeral=True)

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
        # Sync commands
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")

if __name__ == '__main__':
    client.run(TOKEN)