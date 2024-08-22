import logging

import discord
from discord import app_commands
from dotenv import dotenv_values
from supabase import Client

from hazel.services.supabase_client import supabase_client
from hazel.utils.users import check_if_user_exists


class Unregister(app_commands.Group):
    @app_commands.command()
    async def hacker(self, interaction: discord.Interaction):
        logging.info(
            f"Unregister.hacker: received unregister request from {interaction.user}"
        )
        supabase: Client = self.extras["supabase"]

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase, username=interaction.user.name, table="hacker"
        ):
            logging.warning(
                f"Unregister.hacker: {interaction.user} is not registered for the event"
            )
            await interaction.response.send_message(
                "You are not registered for the event", ephemeral=True
            )
            return

        # Unregister user
        logging.info(
            f"Unregister.hacker: unregistering {interaction.user} for the event"
        )
        try:
            supabase: Client = self.extras["supabase"]
            supabase.table("hacker").delete().eq(
                "username", interaction.user.name
            ).execute()
            logging.info(
                f"Unregister.hacker: {interaction.user} unregistered successfully"
            )
            await interaction.response.send_message(
                "You have been unregistered for the event", ephemeral=True
            )
        except Exception as e:
            logging.error(
                f"Unregister.hacker: error while unregistering {interaction.user} for the event: {e}"
            )
            await interaction.response.send_message(
                "An error occurred while unregistering you for the event. Please try again later.",
                ephemeral=True,
            )

    @app_commands.command()
    @app_commands.describe(password="Password provided by an organizer")
    async def mentor(self, interaction: discord.Interaction, password: str):
        logging.info(
            f"Unregister.mentor: received unregister request from {interaction.user}"
        )
        supabase: Client = self.extras["supabase"]
        env: dict[str, str] = self.extras["dotenv"]

        # Check if password is correct
        if password != env["MENTOR_PASSWORD"]:
            logging.warning(
                f"Unregister.mentor: {interaction.user} entered the wrong password"
            )
            await interaction.response.send_message(
                "Incorrect password", ephemeral=True
            )
            return

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase, username=interaction.user.name, table="mentor"
        ):
            logging.warning(
                f"Unregister.mentor: {interaction.user} is not registered for the event"
            )
            await interaction.response.send_message(
                "You are not registered for the event", ephemeral=True
            )
            return

        # Unregister user
        logging.info(
            f"Unregister.mentor: unregistering {interaction.user} for the event"
        )
        try:
            supabase: Client = self.extras["supabase"]
            supabase.table("mentor").delete().eq(
                "username", interaction.user.name
            ).execute()
            logging.info(
                f"Unregister.mentor: {interaction.user} unregistered successfully"
            )
            await interaction.response.send_message(
                "You have been unregistered for the event", ephemeral=True
            )
        except Exception as e:
            logging.error(
                f"Unregister.mentor: error while unregistering {interaction.user} for the event: {e}"
            )
            await interaction.response.send_message(
                "An error occurred while unregistering you for the event. Please try again later.",
                ephemeral=True,
            )


async def setup(client: discord.Client):
    logging.info("Unregister: registering slash command")
    client.tree.add_command(
        Unregister(
            name="unregister",
            description="Unregister a user for the event",
            extras={"supabase": supabase_client, "dotenv": dotenv_values()},
        )
    )
