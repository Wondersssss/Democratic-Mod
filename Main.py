#FIXME: Add option to disable admin perms for vote
#FIXME: Fix file mismanagement errors

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
import VoteButtons
from Commands import setupCommands
from TestCommands import setupTestCommands
#========================

# GET TOKEN
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(f"Bot token: {TOKEN}")

ADMIN_ONLY = True
active_votes = []

# BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # Needed for message commands
intents.voice_states = True     # Needed for voice channel operations
client: Client = Client(intents=intents)
tree = app_commands.CommandTree(client)  # Explicit command tree creation
print("Bot intents/command tree initialised!")


VOTE_START_PATH: Final[str] = "sounds/voteStart.wav"

async def initiateVote(interaction: discord.Interaction, type: str, userTarget: discord.Member):
    if interaction.guild_id in active_votes:
        await interaction.response.send_message("There's already an active vote in this server!", ephemeral=True)
        print(f"Vote cancelled due to one ongoing in {interaction.guild.name}.")
        return
    
    # Store the active vote
    active_votes.append(interaction.guild.id)

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
    if vc.is_connected:
        print(f"Attempting to play {file}...")
        vc.play(file, after=lambda e: print(f"Player error: {e}"))
        print(f"{file} played!")
    else:
        print("ERROR: Bot isn't in VC")
        await interaction.response.send_message("Bot isn't in VC!", ephemeral=True)



# COMMAND SYNC
@client.event
async def on_ready():
    print(f"{client.user.name} is now online!")
    print("Syncing commands...")
    try:
        setupCommands(tree)
        setupTestCommands(tree)
        synced = await tree.sync()
        print(f"All {len(synced)} commands successfully synced!")
    except Exception as e:
        print(f"Command syncing unsuccessful: {e}")

if __name__ == '__main__':
    # So every import doesn't try to run the bot
    client.run(token=TOKEN)


