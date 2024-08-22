import logging
import os

import discord
from discord import app_commands
from dotenv import load_dotenv
from supabase import Client

from hazel.services.supabase_client import supabase_client
from hazel.utils.constants import *
from hazel.utils.users import check_if_user_exists, check_root_leaf_branch


class Update(app_commands.Group):
    @app_commands.command(
        description="Update skills, root, branch and leaf in the event database for hackers"
    )
    async def hacker(self, interaction: discord.Interaction):
        logging.info("Update.hacker: received update request from {interaction.user}")
        supabase: Client = self.extras["supabase"]
        discord_client: discord.Client = self.extras["client"]

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase, username=interaction.user.name, table="hacker"
        ):
            logging.warning(
                f"Update.hacker: {interaction.user} is not registered for the event"
            )
            await interaction.response.send_message(
                "You are not registered for the event. Try /register hacker",
                ephemeral=True,
            )
            return

        # Check if user has exactly 1 root role, 1 leaf role, and 1 branch role
        user_roles = [role.name.lower() for role in interaction.user.roles]
        if not check_root_leaf_branch(user_roles):
            logging.warning(
                f"Update.hacker: {interaction.user} does not have the required roles. Roles: {user_roles}"
            )
            reaction_roles_channel = discord.utils.get(
                discord_client.get_all_channels(), name="🎭reaction-roles"
            )
            await interaction.response.send_message(
                f"You do not have the required roles to update for the event. Please make sure you have exactly one root role, one leaf role, and one branch role. Modify your roles by reacting at {reaction_roles_channel.mention} and try again, or contact an organizer.",
                ephemeral=True,
            )
            return

        # Update user skills
        logging.info(
            f"Update.hacker: updating {interaction.user}'s skills for the event"
        )
        try:
            skills = [i for i in user_roles if i not in STRUCTURE_ROLES]
            root = [i for i in user_roles if i in ROOT_ROLES][0]
            leaf = [i for i in user_roles if i in LEAF_ROLES][0]
            branch = [i for i in user_roles if i in BRANCH_ROLES][0]
            supabase.table("hacker").update(
                {
                    "root": root,
                    "leaf": leaf,
                    "branch": branch,
                    "skills": skills,
                }
            ).eq("username", interaction.user.name).execute()
            logging.info(
                f"Update.hacker: {interaction.user}'s skills updated successfully"
            )
            await interaction.response.send_message(
                "Your skills, root, branch and leaf have been updated", ephemeral=True
            )
        except Exception as e:
            logging.error(
                f"Update.hacker: error while updating {interaction.user}'s skills for the event: {e}"
            )
            await interaction.response.send_message(
                "An error occurred while updating your skills for the event. Please try again later.",
                ephemeral=True,
            )

    @app_commands.command(
        description="Update root, branch and leaf in the event database for mentors"
    )
    @app_commands.describe(password="Password provided by an organizer")
    async def mentor(self, interaction: discord.Interaction, password: str):
        logging.info(f"Update.mentor: received update request from {interaction.user}")
        supabase: Client = self.extras["supabase"]
        discord_client: discord.Client = self.extras["client"]

        # Check if password is correct
        if password != os.getenv("MENTOR_PASSWORD"):
            logging.warning(
                f"Register.mentor: {interaction.user} entered an incorrect password"
            )
            await interaction.response.send_message(
                "Incorrect password. Please try again or contact an organizer for help.",
                ephemeral=True,
            )
            return

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase, username=interaction.user.name, table="mentor"
        ):
            logging.warning(
                f"Register.mentor: {interaction.user} is not registered for the event"
            )
            await interaction.response.send_message(
                "You are not registered for the event. Try /register mentor password:<insert password given>",
                ephemeral=True,
            )
            return

        # Check if user has exactly 1 root role, 1 leaf role, and 1 branch role
        user_roles = [role.name.lower() for role in interaction.user.roles]
        if not check_root_leaf_branch(user_roles):
            logging.warning(
                f"Register.mentor: {interaction.user} does not have the required roles. Roles: {user_roles}"
            )
            reaction_roles_channel = discord.utils.get(
                discord_client.get_all_channels(), name="🎭reaction-roles"
            )
            await interaction.response.send_message(
                f"You do not have the required roles to register for the event. Please make sure you have exactly one root role, one leaf role, and one branch role. Modify your roles by reacting at {reaction_roles_channel.mention} and try again, or contact an organizer.",
                ephemeral=True,
            )
            return

        # Update user info
        logging.info(f"Update.mentor: updating {interaction.user}'s info for the event")
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
                f"Update.mentor: {interaction.user}'s skills updated successfully"
            )
            await interaction.response.send_message(
                "Your root, branch and leaf have been updated", ephemeral=True
            )
        except Exception as e:
            logging.error(
                f"Register.mentor: error while registering {interaction.user} for the event: {e}"
            )
            await interaction.response.send_message(
                "An error occurred while registering you for the event. Please try again later or contact an organizer for help.",
                ephemeral=True,
            )


async def setup(client: discord.Client):
    logging.info("Update: registering slash command")
    load_dotenv()
    client.tree.add_command(
        Update(
            name="update",
            description="Update existing information in the event database",
            extras={
                "supabase": supabase_client,
                "client": client,
            },
        )
    )
