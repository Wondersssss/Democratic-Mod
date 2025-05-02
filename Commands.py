import discord
from discord import app_commands
from Main import *

# List of all commands, they're basically all the same with minor tweaks.
# I made all the actions seperate to avoid confusion.



def setupCommands(tree):

    global ADMIN_ONLY

    @tree.command(name="vote-timeout", description="Vote to timeout user.")
    @app_commands.describe(user="The user to timeout")
    async def voteTimeout(interaction: discord.Interaction, user: discord.Member):
        if ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            interaction.response.send_message("Permission is currently admin only.")
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        if not user.is_timed_out():
            await interaction.response.defer()
            await initiateVote(interaction, "timeout", user)
            print(f"Starting up the timeout vote against {user}...")
        else:
            await interaction.response.send_message(f"{user.name} is already timed out!")
            print(f"ERROR: {user.name} is already timed out while timeout request was made.")

    @tree.command(name="vote-kick", description="Vote to kick user.")
    @app_commands.describe(user="The user to kick")
    async def voteKick(interaction: discord.Interaction, user: discord.Member):
        if ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            interaction.response.send_message("Permission is currently admin only.")
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        await interaction.response.defer()
        await initiateVote(interaction, "kick", user)
        print(f"Starting up the kick vote against {user}...")

    @tree.command(name="vote-ban", description="Vote to ban user.")
    @app_commands.describe(user="The user to ban")
    async def voteBan(interaction: discord.Interaction, user: discord.Member):
        if ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            interaction.response.send_message("Permission is currently admin only.")
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        await interaction.response.defer()
        await initiateVote(interaction, "ban", user)
        print(f"Starting up the ban vote against {user}...")

    @tree.command(name="vote-mute", description="Vote to mute user.")
    @app_commands.describe(user="The user to mute")
    async def voteMute(interaction: discord.Interaction, user: discord.Member):
        if ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            interaction.response.send_message("Permission is currently admin only.")
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        if not user.voice.mute:
            await interaction.response.defer()
            await initiateVote(interaction, "mute", user)
            print(f"Starting up the mute vote against {user}...")
        else:
            await interaction.response.send_message(f"{user.name} is already muted!")
            print(f"ERROR: {user.name} is already muted while mute request was made.")

    @tree.command(name="vote-unmute", description="Vote to unmute user.")
    @app_commands.describe(user="The user to unmute")
    async def voteUnmute(interaction: discord.Interaction, user: discord.Member):
        if ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            interaction.response.send_message("Permission is currently admin only.")
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        if user.voice.mute:
            await interaction.response.defer()
            await initiateVote(interaction, "unmute", user)
            print(f"Starting up the unmute vote against {user}...")
        else:
            await interaction.response.send_message(f"{user.name} is not muted!")
            print(f"ERROR: {user.name} is not muted while unmute request was made.")

    @tree.command(name="vote-deafen", description="Vote to deafen user.")
    @app_commands.describe(user="The user to deafen")
    async def voteDeafen(interaction: discord.Interaction, user: discord.Member):
        if ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            interaction.response.send_message("Permission is currently admin only.")
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        if not user.voice.deaf:
            await interaction.response.defer()
            await initiateVote(interaction, "deafen", user)
            print(f"Starting up the deafen vote against {user}...")
        else:
            await interaction.response.send_message(f"{user.name} is already deafened!")
            print(f"ERROR: {user.name} is already deafened while deafen request was made.")

    @tree.command(name="vote-undeafen", description="Vote to undeafen user.")
    @app_commands.describe(user="The user to undeafen")
    async def voteUndeafen(interaction: discord.Interaction, user: discord.Member):
        if ADMIN_ONLY and not interaction.user.guild_permissions.administrator:
            interaction.response.send_message("Permission is currently admin only.")
            print(f"Vote was cast but {interaction.user.name} is not an admin.")
            return
        if user.voice.deaf:
            await interaction.response.defer()
            await initiateVote(interaction, "undeafen", user)
            print(f"Starting up the undeafen vote against {user}...")
        else:
            await interaction.response.send_message(f"{user.name} is not deafened!")
            print(f"ERROR: {user.name} is not deafened while undeafen request was made.")

    @tree.command(name="toggle-public-permission", description="Toggles the permissions of the vote, meaning anyone can cast it")
    @app_commands.checks.has_permissions(administrator=True)
    async def togglePublicPerms(interaction: discord.Interaction):
        if ADMIN_ONLY:
            ADMIN_ONLY = False
        else:
            ADMIN_ONLY = True
        await interaction.response.send_message(f"Public permissions to vote are now set to {not ADMIN_ONLY}!")
        print(f"Public permission now set to {not ADMIN_ONLY}.")

    @tree.command(name="view-public-permission", description="View the current status of public permission")
    async def viewPublicPerms(interaction: discord.Interaction):
        await interaction.response.send_message(f"Public permission to vote is set to {not ADMIN_ONLY}")
        print(f"Public permission is currently {not ADMIN_ONLY}.")



