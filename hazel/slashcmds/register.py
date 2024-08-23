import logging
import os
from datetime import datetime

import discord
from discord import app_commands
from dotenv import load_dotenv
from supabase import Client

from hazel.services.supabase_client import supabase_client
from hazel.utils.constants import *
from hazel.utils.users import check_if_user_exists, check_root_leaf_branch


class Register(app_commands.Group):
    @app_commands.command(description="Register as a hacker for the event")
    async def hacker(self, interaction: discord.Interaction):
        logging.info(
            f"Register.hacker: received register request from {interaction.user}"
        )
        supabase: Client = self.extras["supabase"]

        # check if it is currently 8AM August 24th 2024
        if datetime.now() < datetime(2024, 8, 24, 8, 0, 0):
            logging.warning(
                f"Register.hacker: {interaction.user} tried to register before the event started"
            )
            await interaction.response.send_message(
                "The event has not started yet. Please try again later.", ephemeral=True
            )
            return

        # Check if user exists in the database
        if check_if_user_exists(
            client=supabase, username=interaction.user.name, table="hacker"
        ):
            logging.warning(
                f"Register.hacker: {interaction.user} is already registered for the event"
            )
            await interaction.response.send_message(
                "You are already registered for the event", ephemeral=True
            )
            return

        # Check if user has exactly 1 root role, 1 leaf role, and 1 branch role
        user_roles = [role.name.lower() for role in interaction.user.roles]
        if not check_root_leaf_branch(user_roles):
            logging.warning(
                f"Register.hacker: {interaction.user} does not have the required roles. Roles: {user_roles}"
            )
            reaction_roles_channel = discord.utils.get(
                interaction.guild.channels, name="🎭reaction-roles"
            )
            await interaction.response.send_message(
                f"You do not have the required roles to register for the event. Please make sure you have exactly one root role, one leaf role, and one branch role. Modify your roles by reacting at {reaction_roles_channel.mention} and try again, or contact an organizer.",
                ephemeral=True,
            )
            return

        # Register user
        logging.info(f"Register.hacker: registering {interaction.user} for the event")
        try:
            skills = [i for i in user_roles if i not in STRUCTURE_ROLES]
            root = [i for i in user_roles if i in ROOT_ROLES][0]
            leaf = [i for i in user_roles if i in LEAF_ROLES][0]
            branch = [i for i in user_roles if i in BRANCH_ROLES][0]
            supabase.table("hacker").insert(
                {
                    "username": interaction.user.name,
                    "root": root,
                    "leaf": leaf,
                    "branch": branch,
                    "skills": skills,
                }
            ).execute()
            logging.info(f"Register.hacker: {interaction.user} registered successfully")
            # give hacker role
            if "hacker" not in user_roles:
                hacker_role = discord.utils.get(interaction.guild.roles, name="Hacker")
                await interaction.user.add_roles(hacker_role)
            await interaction.response.send_message(
                "You have been registered for the event", ephemeral=True
            )
        except Exception as e:
            logging.error(
                f"Register.hacker: error while registering {interaction.user} for the event: {e}"
            )
            await interaction.response.send_message(
                "An error occurred while registering you for the event. Please try again later.",
                ephemeral=True,
            )

    @app_commands.command(description="Register as a mentor for the event")
    @app_commands.describe(password="Password provided by an organizer")
    async def mentor(self, interaction: discord.Interaction, password: str):
        logging.info(
            f"Register.mentor: received register request from {interaction.user}"
        )
        supabase: Client = self.extras["supabase"]

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
        if check_if_user_exists(
            client=supabase, username=interaction.user.name, table="mentor"
        ):
            logging.warning(
                f"Register.mentor: {interaction.user} is already registered for the event"
            )
            await interaction.response.send_message(
                "You are already registered for the event", ephemeral=True
            )
            return

        # Check if user has exactly 1 root role, 1 leaf role, and 1 branch role
        user_roles = [role.name.lower() for role in interaction.user.roles]
        if not check_root_leaf_branch(user_roles, count_leaf=False):
            logging.warning(
                f"Register.mentor: {interaction.user} does not have the required roles. Roles: {user_roles}"
            )
            reaction_roles_channel = discord.utils.get(
                interaction.guild.channels, name="🎭reaction-roles"
            )
            await interaction.response.send_message(
                f"You do not have the required roles to register for the event. Please make sure you have exactly one root role and one branch role. Modify your roles by reacting at {reaction_roles_channel.mention} and try again, or contact an organizer.",
                ephemeral=True,
            )
            return

        # Register user
        logging.info(f"Register.mentor: registering {interaction.user} for the event")
        try:
            root = [i for i in user_roles if i in ROOT_ROLES][0]
            branch = [i for i in user_roles if i in BRANCH_ROLES][0]
            supabase.table("mentor").insert(
                {
                    "username": interaction.user.name,
                    "root": root,
                    "branch": branch,
                }
            ).execute()
            logging.info(f"Register.mentor: {interaction.user} registered successfully")
            # give mentor role
            if "mentor" not in user_roles:
                mentor_role = discord.utils.get(interaction.guild.roles, name="Mentor")
                await interaction.user.add_roles(mentor_role)
            await interaction.response.send_message(
                "You have been registered for the event", ephemeral=True
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
    logging.info("Register: registering slash command")
    load_dotenv()
    client.tree.add_command(
        Register(
            name="register",
            description="Register a user for the event",
            extras={
                "supabase": supabase_client,
            },
        )
    )
