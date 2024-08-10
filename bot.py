import asyncio
import logging
import os
from datetime import datetime
from sys import stdout

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from supabase import Client, create_client

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


class Interests(discord.ui.Modal, title="Interests"):
    interests = discord.ui.TextInput(
        label="List out your interests.",
        style=discord.TextStyle.long,
        placeholder="Type your interests here...",
        required=True,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            logging.info(f"Inputted interests: {self.interests.value}")
            await interaction.response.send_message(f"Interests saved!", ephemeral=True)
            supabase.table("hacker").update({"interests": self.interests.value}).eq(
                "username", interaction.user.name
            ).execute()
        except Exception as e:
            logging.error(
                f"interests: Error saving {interaction.user}'s interests: {e}"
            )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        await interaction.response.send_message(
            "Oops! Something went wrong.", ephemeral=True
        )

        logging.info(type(error), error, error.__traceback__)


@client.tree.command(name="interests", description="Submit what your interests are.")
async def interests(interaction: discord.Interaction):
    await interaction.response.send_modal(Interests())


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
    structure_roles = [
        "@everyone",
        "web",
        "organizer",
        "marketing",
        "logistics",
        "admin",
        "judge",
        "mentor",
        "minor",
        "hacker",
        "sponsorship",
        "branding",
        "marketing",
    ]
    logging.info(f"register: Received register request from {interaction.user}")
    try:
        supabase.table("hacker").insert({"username": interaction.user.name}).execute()

        hacker = (
            supabase.table("hacker")
            .select("*")
            .eq("username", interaction.user.name)
            .execute()
        )

        if hacker.data:
            roles = [i.name for i in interaction.user.roles]
            print("Roles: ", roles)

            for role in roles:
                if role.lower() not in structure_roles:
                    response = (
                        supabase.table("skills")
                        .insert({"user_id": hacker.data[0]["id"], "skill": role})
                        .execute()
                    )
                    print("Response: ", response.data)
    except Exception as e:
        logging.error(f"register: Error registering {interaction.user}: {e}")
        # 23505 - User is already registered
        if e.code == "23505":
            await interaction.response.send_message(
                "You are already registered.", ephemeral=True
            )
            return

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
        # get the hacker id, then delete the hacker and their skills
        hacker = (
            supabase.table("hacker")
            .select("*")
            .eq("username", interaction.user.name)
            .execute()
        )
        if hasattr(hacker, "data") and hacker.data:
            skills = (
                supabase.table("skills")
                .select("*")
                .eq("user_id", hacker.data[0]["id"])
                .execute()
            )
            for skill in skills.data:
                supabase.table("skills").delete().eq("id", skill["id"]).execute()

        supabase.table("hacker").delete().eq(
            "username", interaction.user.name
        ).execute()
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
        hacker = (
            supabase.table("hacker")
            .select("*")
            .eq("username", interaction.user.name)
            .execute()
        )

        skills = (
            supabase.table("skills")
            .select("*")
            .eq("user_id", hacker.data[0]["id"])
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

    if not hacker.data:
        logging.info(f"display_profile: No profile found for {interaction.user}")
        await interaction.response.send_message("No profile found.", ephemeral=True)
        return
    logging.info(f"display_profile: Displaying profile for {interaction.user}")
    parsed_skills = [skill["skill"] for skill in skills.data]

    profile_string = f"ID: {hacker.data[0]['id']}\nUsername: {hacker.data[0]['username']}\nSkills: {parsed_skills}\nInterests: \"{hacker.data[0]['interests']}\"\nJoined at: {hacker.data[0]['joined_at']}\nJoined matchmaking: {bool(hacker.data[0]['joined_matchmaking'])}\nMatchmade: {bool(hacker.data[0]['matchmade'])}"
    await interaction.response.send_message(profile_string, ephemeral=True)


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
