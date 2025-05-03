import discord
from discord import app_commands
from discord.ext import commands
import datetime
from Main import initiateVote

# List of all commands, they're basically all the same with minor tweaks, EXCEPT the admin settings at the bottom
# I made all the actions seperate to avoid confusion.

class Commands(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client
        self.ADMIN_ONLY = True

    async def permission_checks(self, user: discord.Member, interaction: discord.Interaction) -> bool:
        if user == interaction.guild.owner:
            await interaction.followup.send("You can't vote against the server owner!", ephemeral=True)
            print("Vote tried on server owner, failed.")
            return False
        if self.ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            await interaction.followup.send("You do not have permission to use this command.", ephemeral=True)
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return False
        return True




    @app_commands.command(name="vote-timeout", description="Vote to timeout user.")
    @app_commands.describe(user="The user to timeout")

    async def voteTimeout(self, interaction: discord.Interaction, user: discord.Member):
        if not user.is_timed_out():
            await interaction.response.defer()
            if not await self.permission_checks(user, interaction):
                return
            await initiateVote(interaction, "timeout", user)
            print(f"Starting up the timeout vote against {user}...")
        else:
            await interaction.followup.send(f"{user.name} is already timed out!", ephemeral=True)
            print(f"ERROR: {user.name} is already timed out while timeout request was made.")

    @app_commands.command(name="vote-kick", description="Vote to kick user.")
    @app_commands.describe(user="The user to kick")

    async def voteKick(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer()
        if not await self.permission_checks(user, interaction):
            return
        await initiateVote(interaction, "kick", user)
        print(f"Starting up the kick vote against {user}...")

    @app_commands.command(name="vote-ban", description="Vote to ban user.")
    @app_commands.describe(user="The user to ban")

    async def voteBan(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer()
        if not await self.permission_checks(user, interaction):
            return
        await initiateVote(interaction, "ban", user)
        print(f"Starting up the ban vote against {user}...")

    @app_commands.command(name="vote-mute", description="Vote to mute user.")
    @app_commands.describe(user="The user to mute")

    async def voteMute(self, interaction: discord.Interaction, user: discord.Member):
        if not user.voice.mute:
            await interaction.response.defer()
            if not await self.permission_checks(user, interaction):
                return
            await initiateVote(interaction, "mute", user)
            print(f"Starting up the mute vote against {user}...")
        else:
            await interaction.followup.send(f"{user.name} is already muted!", ephemeral=True)
            print(f"{user.name} is already muted while mute request was made.")

    @app_commands.command(name="vote-unmute", description="Vote to unmute user.")
    @app_commands.describe(user="The user to unmute")

    async def voteUnmute(self, interaction: discord.Interaction, user: discord.Member):
        if user.voice.mute:
            if not await self.permission_checks(user, interaction):
                return
            await interaction.response.defer()
            await initiateVote(interaction, "unmute", user)
            print(f"Starting up the unmute vote against {user}...")
        else:
            await interaction.followup.send(f"{user.name} is not muted!", ephemeral=True)
            print(f"{user.name} is not muted while unmute request was made.")

    @app_commands.command(name="vote-deafen", description="Vote to deafen user.")
    @app_commands.describe(user="The user to deafen")

    async def voteDeafen(self, interaction: discord.Interaction, user: discord.Member):
        if not user.voice.deaf:
            if not await self.permission_checks(user, interaction):
                return
            await interaction.response.defer()
            await initiateVote(interaction, "deafen", user)
            print(f"Starting up the deafen vote against {user}...")
        else:
            await interaction.followup.send(f"{user.name} is already deafened!", ephemeral=True)
            print(f"{user.name} is already deafened while deafen request was made.")

    @app_commands.command(name="vote-undeafen", description="Vote to undeafen user.")
    @app_commands.describe(user="The user to undeafen")

    async def voteUndeafen(self, interaction: discord.Interaction, user: discord.Member):
        if user.voice.deaf:
            await interaction.response.defer()
            if not await self.permission_checks(user, interaction):
                return
            await initiateVote(interaction, "undeafen", user)
            print(f"Starting up the undeafen vote against {user}...")
        else:
            await interaction.followup.send(f"{user.name} is not deafened!", ephemeral=True)
            print(f"{user.name} is not deafened while undeafen request was made.")

    @app_commands.command(name="toggle-public-permission", description="Toggles the permissions of the vote, meaning anyone can cast it")
    @app_commands.checks.has_permissions(administrator=True)

    async def togglePublicPerms(self, interaction: discord.Interaction):
        if self.ADMIN_ONLY:
            self.ADMIN_ONLY = False
        else:
            self.ADMIN_ONLY = True
        await interaction.response.send_message(f"Public permissions to vote are now set to {not self.ADMIN_ONLY}!")
        print(f"Public permission now set to {not self.ADMIN_ONLY}.")

    @app_commands.command(name="view-public-permission", description="View the current status of public permission")
    
    async def viewPublicPerms(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Public permission to vote is set to {not self.ADMIN_ONLY}")
        print(f"Public permission is currently {not self.ADMIN_ONLY}.")

async def setup(client: commands.Bot):
    await client.add_cog(Commands(client))



