import discord
from discord import app_commands
from Main import *
from discord.ext import commands

# List of all commands, they're basically all the same with minor tweaks, EXCEPT the admin settings at the bottom
# I made all the actions seperate to avoid confusion.

class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ADMIN_ONLY = True


    @app_commands.command(name="vote-timeout", description="Vote to timeout user.")
    @app_commands.describe(user="The user to timeout")

    async def voteTimeout(self, interaction: discord.Interaction, user: discord.Member):
        if user == interaction.guild.owner:
            await interaction.response.send_message("You can't timeout the owner of the server!", ephemeral=True)
            print("Vote tried on server owner, failed.")
            return
        if self.ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        if not user.is_timed_out():
            await interaction.response.defer()
            await initiateVote(interaction, "timeout", user)
            print(f"Starting up the timeout vote against {user}...")
        else:
            await interaction.response.send_message(f"{user.name} is already timed out!", ephemeral=True)
            print(f"ERROR: {user.name} is already timed out while timeout request was made.")

    @app_commands.command(name="vote-kick", description="Vote to kick user.")
    @app_commands.describe(user="The user to kick")

    async def voteKick(self, interaction: discord.Interaction, user: discord.Member):
        if user == interaction.guild.owner:
            await interaction.response.send_message("You can't kick the owner of the server!", ephemeral=True)
            print("Vote tried on server owner, failed.")
            return
        if self.ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Permission is currently admin only.", ephemeral=True)
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        await interaction.response.defer()
        await initiateVote(interaction, "kick", user)
        print(f"Starting up the kick vote against {user}...")

    @app_commands.command(name="vote-ban", description="Vote to ban user.")
    @app_commands.describe(user="The user to ban")

    async def voteBan(self, interaction: discord.Interaction, user: discord.Member):
        if user == interaction.guild.owner:
            await interaction.response.send_message("You can't ban the owner of the server!", ephemeral=True)
            print("Vote tried on server owner, failed.")
            return
        if self.ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Permission is currently admin only.", ephemeral=True)
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        await interaction.response.defer()
        await initiateVote(interaction, "ban", user)
        print(f"Starting up the ban vote against {user}...")

    @app_commands.command(name="vote-mute", description="Vote to mute user.")
    @app_commands.describe(user="The user to mute")

    async def voteMute(self, interaction: discord.Interaction, user: discord.Member):
        if user == interaction.guild.owner:
            await interaction.response.send_message("You can't mute the owner of the server!", ephemeral=True)
            print("Vote tried on server owner, failed.")
            return
        if self.ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Permission is currently admin only.", ephemeral=True)
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        if not user.voice.mute:
            await interaction.response.defer()
            await initiateVote(interaction, "mute", user)
            print(f"Starting up the mute vote against {user}...")
        else:
            await interaction.response.send_message(f"{user.name} is already muted!", ephemeral=True)
            print(f"{user.name} is already muted while mute request was made.")

    @app_commands.command(name="vote-unmute", description="Vote to unmute user.")
    @app_commands.describe(user="The user to unmute")

    async def voteUnmute(self, interaction: discord.Interaction, user: discord.Member):
        if user == interaction.guild.owner:
            await interaction.response.send_message("You can't unmute the owner of the server!", ephemeral=True)
            print("Vote tried on server owner, failed.")
            return
        if self.ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Permission is currently admin only.", ephemeral=True)
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        if user.voice.mute:
            await interaction.response.defer()
            await initiateVote(interaction, "unmute", user)
            print(f"Starting up the unmute vote against {user}...")
        else:
            await interaction.response.send_message(f"{user.name} is not muted!", ephemeral=True)
            print(f"{user.name} is not muted while unmute request was made.")

    @app_commands.command(name="vote-deafen", description="Vote to deafen user.")
    @app_commands.describe(user="The user to deafen")

    async def voteDeafen(self, interaction: discord.Interaction, user: discord.Member):
        if user == interaction.guild.owner:
            await interaction.response.send_message("You can't deafen the owner of the server!", ephemeral=True)
            print("Vote tried on server owner, failed.")
            return
        if self.ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Permission is currently admin only.", ephemeral=True)
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        if not user.voice.deaf:
            await interaction.response.defer()
            await initiateVote(interaction, "deafen", user)
            print(f"Starting up the deafen vote against {user}...")
        else:
            await interaction.response.send_message(f"{user.name} is already deafened!", ephemeral=True)
            print(f"{user.name} is already deafened while deafen request was made.")

    @app_commands.command(name="vote-undeafen", description="Vote to undeafen user.")
    @app_commands.describe(user="The user to undeafen")

    async def voteUndeafen(self, interaction: discord.Interaction, user: discord.Member):
        if user == interaction.guild.owner:
            await interaction.response.send_message("You can't undeafen the owner of the server!", ephemeral=True)
            print("Vote tried on server owner, failed.")
            return
        if self.ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Permission is currently admin only.", ephemeral=True)
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        if user.voice.deaf:
            await interaction.response.defer()
            await initiateVote(interaction, "undeafen", user)
            print(f"Starting up the undeafen vote against {user}...")
        else:
            await interaction.response.send_message(f"{user.name} is not deafened!", ephemeral=True)
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

async def command_setup(client):
    await client.add_cog(Commands(client))



