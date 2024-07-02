import asyncio
import logging
import os
import sqlite3
from datetime import datetime
from sys import stdout

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(stdout),
        logging.FileHandler(
            f"hazel/logs/hazel-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.log"
        ),
    ],
)

# exit if the database does not exist
# if "data.db" not in os.listdir("hazel"):
#     logging.error("main: Database does not exist, exiting")
#     exit(1)


@client.event
async def on_ready():
    # sync current commands with the fodh server for quick development
    await client.tree.sync(guild=discord.Object(id=os.getenv("FODH_GUILD_ID")))
    logging.info(f"on_ready: {client.user} has connected to Discord!")


@client.tree.command(name="ping", description="Check the bot's latency.")
async def ping(interaction: discord.Interaction):
    logging.info(f"ping: Received ping request from {interaction.user}")
    await interaction.response.send_message(
        f"Pong! {round(client.latency * 1000)}ms", ephemeral=True
    )


@client.tree.command(
    name="register", description="Register as a hacker for matchmaking."
)
async def register(interaction: discord.Interaction):
    logging.info(f"register: Received register request from {interaction.user}")
    try:
        supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        response = (
            supabase.table("HACKER")
            .insert({"username": interaction.user.name})
            .execute()
        )
    except Exception as e:
        logging.error(f"register: Error registering {interaction.user}: {e}")
        await interaction.response.send_message(
            "An error occurred while registering.", ephemeral=True
        )
        return
    logging.info(f"register: Registered {interaction.user} as a hacker")
    await interaction.response.send_message("Registered as a hacker.", ephemeral=True)


@client.tree.command(
    name="unregister", description="Unregister as a hacker for matchmaking."
)
async def unregister(interaction: discord.Interaction):
    logging.info(f"unregister: Received unregister request from {interaction.user}")
    try:
        supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        response = (
            supabase.table("HACKER")
            .delete()
            .eq("username", interaction.user.name)
            .execute()
        )
    except Exception as e:
        logging.error(f"unregister: Error unregistering {interaction.user}: {e}")
        await interaction.response.send_message(
            "An error occurred while unregistering.", ephemeral=True
        )
        return
    logging.info(f"unregister: Unregistered {interaction.user} as a hacker")
    await interaction.response.send_message("Unregistered as a hacker.", ephemeral=True)


@client.tree.command(name="display_profile", description="Display your profile.")
async def display_profile(interaction: discord.Interaction):
    logging.info(
        f"display_profile: Received display profile request from {interaction.user}"
    )
    try:
        supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        response = (
            supabase.table("HACKER")
            .select("*")
            .eq("username", interaction.user.name)
            .execute()
        )
    except Exception as e:
        logging.error(
            f"display_profile: Error displaying profile for {interaction.user}: {e}"
        )
        await interaction.response.send_message(
            "An error occurred while displaying your profile.", ephemeral=True
        )
        return
    if not response:
        logging.info(f"display_profile: No profile found for {interaction.user}")
        await interaction.response.send_message("No profile found.", ephemeral=True)
        return
    logging.info(f"display_profile: Displaying profile for {interaction.user}")
    # Untested formatting
    # profile_string = f"ID: {response["data"][0]["ID"]}\nUsername: {response["data"][0]["USERNAME"]}\nSkills: {response["data"][0]["SKILLS"]}\nJoined at: {result["data"][0]["JOINED_AT"]}\nJoined matchmaking: {bool(result["data"][0]["JOINED_MATCHMAKING"])}\nMatchmade: {bool(result["data"][0]["MATCHMADE"])}"
    # await interaction.response.send_message(profile_string, ephemeral=True)


async def main():
    try:
        async with client:
            client.tree.copy_global_to(
                guild=discord.Object(id=os.getenv("FODH_GUILD_ID"))
            )
            await client.start(os.getenv("HAZEL_TOKEN"))
    except Exception as e:
        logging.error(f"main: Error starting Hazel: {e}")
        await client.close()


if __name__ == "__main__":
    logging.info("main: Starting Hazel bot")
    asyncio.run(main())
