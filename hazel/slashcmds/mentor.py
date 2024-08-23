import logging
import os

import discord
from discord import app_commands
from dotenv import load_dotenv
from supabase import Client

from hazel.services.supabase_client import supabase_client
from hazel.utils.constants import *
from hazel.utils.users import check_if_user_exists, check_root_leaf_branch


class Mentor(app_commands.Group):
    @app_commands.command(description="Register as a mentor for the event")
    async def register(self, interaction: discord.Interaction, password: str):
        logging.info(
            f"Mentor.register: received register request from {interaction.user}"
        )
        supabase: Client = self.extras["supabase"]

        await interaction.response.defer(ephemeral=True)

        # check if the password is correct
        if password != os.getenv("MENTOR_PASSWORD"):
            logging.warning(
                f"Mentor.register: {interaction.user} tried to register with the wrong password `{password}`"
            )
            await interaction.followup.send(
                "The password you entered is incorrect. Please try again.",
                ephemeral=True,
            )
            return

        # Check if user exists in the database
        if check_if_user_exists(
            client=supabase, username=interaction.user.name, table="mentor"
        ):
            logging.warning(
                f"Mentor.register: {interaction.user} is already registered for the event"
            )
            await interaction.followup.send(
                "You are already registered for the event", ephemeral=True
            )
            return

        # Check if user has exactly 1 root role and 1 branch role
        user_roles = [role.name.lower() for role in interaction.user.roles]
        if not check_root_leaf_branch(user_roles, count_leaf=False):
            logging.warning(
                f"Mentor.register: {interaction.user} does not have the required roles. Roles: {user_roles}"
            )
            reaction_roles_channel = discord.utils.get(
                interaction.guild.channels, name="🎭reaction-roles"
            )
            await interaction.followup.send(
                f"You do not have the required roles to register for the event. Please make sure you have exactly one root role and one branch role. Modify your roles by reacting at {reaction_roles_channel.mention} and try again, or contact an organizer.",
                ephemeral=True,
            )
            return

        # Register user
        logging.info(f"Mentor.register: registering {interaction.user} for the event")
        try:
            root = [i for i in user_roles if i in ROOT_ROLES][0]
            leaf = [i for i in user_roles if i in LEAF_ROLES][0]
            branch = [i for i in user_roles if i in BRANCH_ROLES][0]
            supabase.table("mentor").insert(
                {
                    "username": interaction.user.name,
                    "root": root,
                    "leaf": leaf,
                    "branch": branch,
                }
            ).execute()
            logging.info(f"Mentor.register: {interaction.user} registered successfully")
            # give mentor role
            if "mentor" not in user_roles:
                mentor_role = discord.utils.get(interaction.guild.roles, name="Mentor")
                await interaction.user.add_roles(mentor_role)
            await interaction.followup.send(
                "You have been registered for the event", ephemeral=True
            )
        except Exception as e:
            logging.error(
                f"Mentor.register: error while registering {interaction.user} for the event: {e}"
            )
            await interaction.followup.send(
                "An error occurred while registering you for the event. Please try again later.",
                ephemeral=True,
            )

    @app_commands.command(description="Update your skills for the event")
    async def update(self, interaction: discord.Interaction, password: str):
        logging.info(f"Mentor.update: received update request from {interaction.user}")
        supabase: Client = self.extras["supabase"]

        await interaction.response.defer(ephemeral=True)

        # check if the password is correct
        if password != os.getenv("MENTOR_PASSWORD"):
            logging.warning(
                f"Mentor.update: {interaction.user} tried to update with the wrong password `{password}`"
            )
            await interaction.followup.send(
                "The password you entered is incorrect. Please try again.",
                ephemeral=True,
            )
            return

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase, username=interaction.user.name, table="mentor"
        ):
            logging.warning(
                f"Mentor.update: {interaction.user} is not registered for the event"
            )
            await interaction.followup.send(
                "You are not registered for the event. Try `/register mentor password:<insert password given>`",
                ephemeral=True,
            )
            return

        # Check if user has exactly 1 root role and 1 branch role
        user_roles = [role.name.lower() for role in interaction.user.roles]
        if not check_root_leaf_branch(user_roles, count_leaf=False):
            logging.warning(
                f"Mentor.update: {interaction.user} does not have the required roles. Roles: {user_roles}"
            )
            reaction_roles_channel = discord.utils.get(
                interaction.guild.channels, name="🎭reaction-roles"
            )
            await interaction.followup.send(
                f"You do not have the required roles to update for the event. Please make sure you have exactly one root role and one branch role. Modify your roles by reacting at {reaction_roles_channel.mention} and try again, or contact an organizer.",
                ephemeral=True,
            )
            return

        # Update user skills
        logging.info(
            f"Mentor.update: updating {interaction.user}'s skills for the event"
        )
        try:
            root = [i for i in user_roles if i in ROOT_ROLES][0]
            leaf = [i for i in user_roles if i in LEAF_ROLES][0]
            branch = [i for i in user_roles if i in BRANCH_ROLES][0]
            supabase.table("mentor").update(
                {
                    "root": root,
                    "leaf": leaf,
                    "branch": branch,
                }
            ).eq("username", interaction.user.name).execute()
            logging.info(
                f"Mentor.update: {interaction.user}'s skills updated successfully"
            )
            await interaction.followup.send(
                "Your skills, root, branch and leaf have been updated", ephemeral=True
            )
        except Exception as e:
            logging.error(
                f"Mentor.update: error while updating {interaction.user}'s skills for the event: {e}"
            )
            await interaction.followup.send(
                "An error occurred while updating your skills for the event. Please try again later.",
                ephemeral=True,
            )

    @app_commands.command(description="Display your stored profile")
    async def display(self, interaction: discord.Interaction, password: str):
        logging.info(
            f"Mentor.display: received display request from {interaction.user}"
        )
        supabase: Client = self.extras["supabase"]

        await interaction.response.defer(ephemeral=True)

        # check if the password is correct
        if password != os.getenv("MENTOR_PASSWORD"):
            logging.warning(
                f"Mentor.display: {interaction.user} tried to display with the wrong password `{password}`"
            )
            await interaction.followup.send(
                "The password you entered is incorrect. Please try again.",
                ephemeral=True,
            )
            return

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase, username=interaction.user.name, table="mentor"
        ):
            logging.warning(
                f"Mentor.display: {interaction.user} is not registered for the event"
            )
            await interaction.followup.send(
                "You are not registered for the event. Try `/register mentor password:<insert password given>`",
                ephemeral=True,
            )
            return

        # Display user profile
        logging.info(
            f"Mentor.display: displaying {interaction.user}'s profile for the event"
        )
        try:
            profile = (
                supabase.table("mentor")
                .select("*")
                .eq("username", interaction.user.name)
                .execute()
                .data[0]
            )
            profile_embed = discord.Embed(
                title=f"{interaction.user.name}'s Profile",
                description=f"**Root**: {profile['root']}\n**Leaf**: {profile['leaf']}\n**Branch**: {profile['branch']}\n**Skills**: {', '.join(profile['skills'])}",
                color=discord.Color.blurple(),
            )
            await interaction.followup.send(embed=profile_embed, ephemeral=True)

        except Exception as e:
            logging.error(
                f"Mentor.display: error while displaying {interaction.user}'s profile for the event: {e}"
            )
            await interaction.followup.send(
                "An error occurred while displaying your profile for the event. Please try again later.",
                ephemeral=True,
            )


async def setup(client: discord.Client):
    logging.info("Register: registering slash command")
    load_dotenv()
    client.tree.add_command(
        Mentor(
            name="mentor",
            description="Commands for mentors",
            extras={
                "supabase": supabase_client,
            },
        )
    )
