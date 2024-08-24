import logging
import os

import discord
from discord import app_commands
from dotenv import load_dotenv
from supabase import Client

from hazel.services.supabase_client import supabase_client
from hazel.utils.constants import *
from hazel.utils.users import check_if_user_exists


class Judge(app_commands.Group):
    @app_commands.command(description="Register as a Judge for the event")
    async def register(self, interaction: discord.Interaction, password: str):
        logging.info(
            f"Judge.register: received register request from {interaction.user}"
        )
        supabase: Client = self.extras["supabase"]

        await interaction.response.defer(ephemeral=True)

        # check if the password is correct
        if password != os.getenv("JUDGE_PASSWORD"):
            logging.warning(
                f"Judge.register: {interaction.user} tried to register with the wrong password `{password}`"
            )
            await interaction.followup.send(
                "The password you entered is incorrect. Please try again.",
                ephemeral=True,
            )
            return

        # Check if user exists in the database
        if check_if_user_exists(
            client=supabase, username=interaction.user.name, table="jusge"
        ):
            logging.warning(
                f"Judge.register: {interaction.user} is already registered for the event"
            )
            await interaction.followup.send(
                "You are already registered for the event", ephemeral=True
            )
            return

        # Register user
        user_roles = [role.name.lower() for role in interaction.user.roles]
        logging.info(f"Judge.register: registering {interaction.user} for the event")
        try:
            supabase.table("judge").insert(
                {
                    "username": interaction.user.name,
                }
            ).execute()
            logging.info(f"Judge.register: {interaction.user} registered successfully")
            # give judge role
            if "judge" not in user_roles:
                judge_role = discord.utils.get(interaction.guild.roles, name="Judge")
                await interaction.user.add_roles(judge_role)
            await interaction.followup.send(
                "You have been registered for the event", ephemeral=True
            )
        except Exception as e:
            logging.error(
                f"Judge.register: error while registering {interaction.user} for the event: {e}"
            )
            await interaction.followup.send(
                "An error occurred while registering you for the event. Please try again later.",
                ephemeral=True,
            )


async def setup(client: discord.Client):
    logging.info("Judge: registering slash command")
    load_dotenv()
    client.tree.add_command(
        Judge(
            name="judge",
            description="Commands for judges",
            extras={
                "supabase": supabase_client,
            },
        )
    )
