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

optionList = ["time out", "timeout", "kick", "ban", "mute", "deafen", "unmute", "undeafen"]

async def initiateVote(interaction: discord.Interaction, type: str, userTarget: discord.Member):
    if interaction.user.voice:
        try:
            # Voice channel connection logic
            channel = interaction.message.author.voice.channel
            vc = await channel.connect(self_deaf=True)
            print(f"Bot has joined {channel.name}, attempting to play the vote start sound...")
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


@client.tree.command(name="Vote", description="Vote to punish user.")
@app_commands.describe(user="The user to punish", action="Type of punishment")
@app_commands.checks.has_permissions(administrator=True)
async def vote(interaction: discord.Interaction, user: discord.Member, action: str):
    # FIXME: ADD CHECK FOR MUTED/DEAFENED and vice versa
    await interaction.response.defer()
    typeAction = action.lower().strip()
    if typeAction in optionList:
        if "-" in typeAction:
            typeAction.replace("-", "")
        await initiateVote(interaction, typeAction, user)
        print(f"Starting up the {typeAction} vote against {user}...")
    else:
        await interaction.response.send_message("Type of punishment invalid. See /help for the list!", ephemeral=True)

@client.tree.command(name="Help", description="Brief overview of the bot & types of punishment")
async def help(interaction: discord.Interaction):
    await interaction.response("Hello! I am the democratic bot, a friend to allow punishing members by voting." \
    "\n\n Here's the list of types you can use for /Vote:" \
    "\n- Kick" \
    "\n- Ban" \
    "\n- Time out" \
    "\n- Mute" \
    "\n- Deafen" \
    "\n\n However only admins can call the command, have fun!")


async def playAudio(file, vc: discord.VoiceClient, interaction: discord.Interaction):
    if interaction.user.voice and vc.is_connected:
        vc.play(file, after=lambda e: print(f"Player error: {e}"))
    else:
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



