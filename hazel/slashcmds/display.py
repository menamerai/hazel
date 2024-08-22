import logging

import discord
from discord import app_commands
from dotenv import dotenv_values
from supabase import Client

from hazel.services.supabase_client import supabase_client
from hazel.utils.users import check_if_user_exists


class Display(app_commands.Group):
    @app_commands.command()
    async def hacker(self, interaction: discord.Interaction):
        logging.info(
            f"Display.hacker: received display request from {interaction.user}"
        )
        supabase: Client = self.extras["supabase"]

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase, username=interaction.user.name, table="hacker"
        ):
            logging.warning(
                f"Display.hacker: {interaction.user} is not registered for the event"
            )
            await interaction.response.send_message(
                "You are not registered for the event. Try /register hacker",
                ephemeral=True,
            )
            return

        # Display user information
        logging.info(
            f"Display.hacker: displaying {interaction.user}'s information for the event"
        )
        try:
            user = (
                supabase.table("hacker")
                .select("*")
                .eq("username", interaction.user.name)
                .execute()
            )
            logging.info(
                f"Display.hacker: {interaction.user}'s information displayed successfully"
            )
            await interaction.response.send_message(f"```{user}```", ephemeral=True)
        except Exception as e:
            logging.error(
                f"Display.hacker: error while displaying {interaction.user}'s information for the event: {e}"
            )
            await interaction.response.send_message(
                "An error occurred while displaying your information for the event. Please try again later.",
                ephemeral=True,
            )

    @app_commands.command()
    @app_commands.describe(password="Password provided by an organizer")
    async def mentor(self, interaction: discord.Interaction, password: str):
        logging.info(
            f"Display.mentor: received display request from {interaction.user}"
        )
        supabase: Client = self.extras["supabase"]
        env: dict[str, str] = self.extras["dotenv"]

        # Check if password is correct
        if password != env["MENTOR_PASSWORD"]:
            logging.warning(
                f"Display.mentor: {interaction.user} entered an incorrect password"
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
                f"Display.mentor: {interaction.user} is not registered for the event"
            )
            await interaction.response.send_message(
                "You are not registered for the event. Try /register mentor password:<insert password given>",
                ephemeral=True,
            )
            return

        # Display user information
        logging.info(
            f"Display.mentor: displaying {interaction.user}'s information for the event"
        )
        try:
            user = (
                supabase.table("mentor")
                .select("*")
                .eq("username", interaction.user.name)
                .execute()
            )
            logging.info(
                f"Display.mentor: {interaction.user}'s information displayed successfully"
            )
            await interaction.response.send_message(f"```{user}```", ephemeral=True)
        except Exception as e:
            logging.error(
                f"Display.mentor: error while displaying {interaction.user}'s information for the event: {e}"
            )
            await interaction.response.send_message(
                "An error occurred while displaying your information for the event. Please try again later.",
                ephemeral=True,
            )


async def setup(client: discord.Client):
    logging.info("Display: registering slash command")
    client.tree.add_command(
        Display(
            name="display",
            description="Display user information from the event database",
            extras={
                "supabase": supabase_client,
                "dotenv": dotenv_values(),
                "client": client,
            },
        )
    )
