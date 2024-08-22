import asyncio
import logging
import os
import random
from datetime import datetime
from sys import stdout

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from supabase import Client, create_client

from hazel.utils.channels import random_channel_name
from hazel.utils.constants import STRUCTURE_ROLES
from hazel.utils.users import check_if_user_exists, check_root_leaf_branch

load_dotenv()

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

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


@client.event
async def on_ready():
    logging.info(f"on_ready: {client.user} is connecting to Discord...")
    await client.load_extension("hazel.slashcmds.register")
    # TODO: remove this line when bot is ready for production
    await client.load_extension("hazel.slashcmds.unregister")
    # sync current commands with the fodh server for quick development
    client.tree.copy_global_to(guild=discord.Object(id=os.getenv("FODH_GUILD_ID")))
    await client.tree.sync(guild=discord.Object(id=os.getenv("FODH_GUILD_ID")))
    logging.info(f"on_ready: {client.user} has connected to Discord!")


@client.tree.command(name="ping", description="Check the bot's latency.")
async def ping(interaction: discord.Interaction):
    logging.info(f"ping: Received ping request from {interaction.user}")
    await interaction.response.send_message(
        f"Pong! {round(client.latency * 1000)}ms", ephemeral=True
    )


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
