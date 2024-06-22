import asyncio
import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())


@client.event
async def on_ready():
    # sync current commands with the fodh server for quick development
    await client.tree.sync(guild=discord.Object(id=os.getenv("FODH_GUILD_ID")))
    print(f"{client.user} has connected to Discord!")


async def main():
    async with client:
        client.tree.copy_global_to(guild=discord.Object(id=os.getenv("FODH_GUILD_ID")))
        await client.start(os.getenv("HAZEL_TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
