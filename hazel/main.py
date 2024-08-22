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
from hazel.utils.users import check_if_user_exists

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
        label="What would you like to build?",
        style=discord.TextStyle.paragraph,
        placeholder="Ex: Web Development, Machine Learning, etc.",
        required=False,
        default="",
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        logging.info(f"Inputted interests: {self.interests.value}")
        # TODO: check if input is toxic
        supabase.table("hacker").update({"interests": self.interests.value}).eq(
            "username", interaction.user.name
        ).execute()
        await interaction.response.send_message("Interests saved!", ephemeral=True)

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        logging.error(
            f"interests: Error saving {interaction.user}'s interests: {error}"
        )
        await interaction.response.send_message(
            "An error occurred while saving your interests.", ephemeral=True
        )


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
        "sponsor",
        "finance",
        "branding",
        "software hacker",
        "pitch competition hacker",
        "ai track",
        "blockchain track",
        "data visualization track",
        "gaming theme",
        "security theme",
        "finance theme",
        "social impact theme",
        "rai",  # funny role
    ]
    logging.info(f"register: Received register request from {interaction.user}")
    try:
        # Check if user is already registered
        if check_if_user_exists(supabase, interaction.user.name):
            logging.warning(f"register: {interaction.user} is already registered.")
            await interaction.response.send_message(
                "You are already registered.", ephemeral=True
            )
            return

        skills = [
            i.name
            for i in interaction.user.roles
            if i.name.lower() not in structure_roles
        ]
        supabase.table("hacker").insert(
            {"username": interaction.user.name, "skills": skills}
        ).execute()

    except Exception as e:
        logging.error(f"register: Error registering {interaction.user}: {e}")
        # 23505 - User is already registered, violation of unique constraint
        if e.code == "23505":
            await interaction.response.send_message(
                "You are already registered.", ephemeral=True
            )
            return

        await interaction.response.send_message(
            "An error occurred while registering.", ephemeral=True
        )
        return

    logging.info(f"register: Registered {interaction.user} as a hacker.")
    await interaction.response.send_message(
        "Registered as a hacker. You should now do /edit_interests to add your interests.",
        ephemeral=True,
    )


# @client.tree.command(name="edit_interests", description="Edit what your interests are.")
# async def edit_interests(interaction: discord.Interaction):
#     # Check if user is already registered
#     if not check_if_user_exists(supabase, interaction.user.name):
#         logging.warning(f"edit_interests: {interaction.user} is not registered.")
#         await interaction.response.send_message(
#             "You are not registered. Please do /register first.", ephemeral=True
#         )
#         return

#     logging.info(
#         f"edit_interests: Received edit interests request from {interaction.user}"
#     )
#     try:
#         await interaction.response.send_modal(Interests())
#     except Exception as e:
#         logging.error(
#             f"edit_interests: Error editing {interaction.user}'s interests: {e}"
#         )
#         await interaction.response.send_message(
#             "An error occurred while editing your interests.", ephemeral=True
#         )


# @client.tree.command(name="unregister", description="Unregister as a hacker.")
# async def unregister(interaction: discord.Interaction):
#     logging.info(f"unregister: Received unregister request from {interaction.user}")
#     try:
#         # Check if user is already registered
#         user = (
#             supabase.table("hacker")
#             .select("id")
#             .eq("username", interaction.user.name)
#             .execute()
#         )
#         if not user.data:
#             logging.warning(f"unregister: {interaction.user} is not registered.")
#             await interaction.response.send_message(
#                 "You are not registered.", ephemeral=True
#             )
#             return

#         supabase.table("hacker").delete().eq(
#             "username", interaction.user.name
#         ).execute()

#     except Exception as e:
#         logging.error(f"unregister: Error unregistering {interaction.user}: {e}")
#         await interaction.response.send_message(
#             "An error occurred while unregistering.", ephemeral=True
#         )
#         return

#     logging.info(f"unregister: Unregistered {interaction.user} as a hacker.")
#     await interaction.response.send_message("Unregistered as a hacker.", ephemeral=True)


# @client.tree.command(name="join_matchmaking", description="Join the matchmaking queue.")
# async def join_matchmaking(interaction: discord.Interaction):
#     logging.info(
#         f"join_matchmaking: Received join matchmaking request from {interaction.user}"
#     )
#     try:
#         # Check if user is already registered
#         if not check_if_user_exists(supabase, interaction.user.name):
#             logging.warning(f"join_matchmaking: {interaction.user} is not registered.")
#             await interaction.response.send_message(
#                 "You are not registered. Please do /register first.", ephemeral=True
#             )
#             return

#         # set the joined_matchmaking flag to true
#         supabase.table("hacker").update({"joined_matchmaking": True}).eq(
#             "username", interaction.user.name
#         ).execute()

#     except Exception as e:
#         logging.error(
#             f"join_matchmaking: Error joining matchmaking queue {interaction.user}: {e}"
#         )
#         await interaction.response.send_message(
#             "An error occurred while joining the matchmaking queue.", ephemeral=True
#         )
#         return

#     logging.info(f"join_matchmaking: Joined matchmaking queue {interaction.user}.")
#     await interaction.response.send_message(
#         "Joined matchmaking queue. You will be matched with other hackers soon.",
#         ephemeral=True,
#     )


# @client.tree.command(
#     name="leave_matchmaking", description="Leave the matchmaking queue."
# )
# async def leave_matchmaking(interaction: discord.Interaction):
#     logging.info(
#         f"leave_matchmaking: Received leave matchmaking request from {interaction.user}"
#     )
#     try:
#         # Check if user is already registered
#         if not check_if_user_exists(supabase, interaction.user.name):
#             logging.warning(f"leave_matchmaking: {interaction.user} is not registered.")
#             await interaction.response.send_message(
#                 "You are not registered. Please do /register first.", ephemeral=True
#             )
#             return

#         # set the joined_matchmaking flag to false
#         supabase.table("hacker").update({"joined_matchmaking": False}).eq(
#             "username", interaction.user.name
#         ).execute()

#     except Exception as e:
#         logging.error(
#             f"leave_matchmaking: Error leaving matchmaking queue {interaction.user}: {e}"
#         )
#         await interaction.response.send_message(
#             "An error occurred while leaving the matchmaking queue.", ephemeral=True
#         )
#         return

#     logging.info(f"leave_matchmaking: Left matchmaking queue {interaction.user}.")
#     await interaction.response.send_message("Left matchmaking queue.", ephemeral=True)


# # TODO: add parameter to specify the maximum members in a team
# @client.tree.command(
#     name="start_random_matchmaking", description="Start random matchmaking."
# )
# async def start_random_matchmaking(interaction: discord.Interaction):
#     # make sure the user has the Web role
#     if "web" not in [i.name.lower() for i in interaction.user.roles]:
#         logging.warning(
#             f"start_random_matchmaking: {interaction.user} does not have the Web role."
#         )
#         await interaction.response.send_message(
#             "You do not have the Web role. Only people with the Web role can start the matchmaking process.",
#             ephemeral=True,
#         )
#         return

#     logging.info(
#         f"start_random_matchmaking: Received start random matchmaking request from {interaction.user}"
#     )

#     try:
#         # get all hackers who have joined the matchmaking queue
#         hackers = (
#             supabase.table("hacker")
#             .select("username")
#             .eq("joined_matchmaking", True)
#             .execute()
#         )
#         hackers = hackers.data

#         # shuffle the hackers
#         random.shuffle(hackers)

#         # match the hackers in maximum teams of 4
#         teams = [hackers[i : i + 4] for i in range(0, len(hackers), 4)]

#         # TODO: proper error handling here, lots of things can go wrong
#         # create a new text channel and voice channel for each team
#         for team in teams:
#             team_name = random_channel_name()
#             # check if a channel with the same name already exists
#             while discord.utils.get(
#                 interaction.guild.text_channels, name=team_name
#             ) or discord.utils.get(interaction.guild.voice_channels, name=team_name):
#                 team_name = random_channel_name()
#             logging.info(
#                 f"start_random_matchmaking: Creating team {team_name} for {team}"
#             )
#             category = discord.utils.get(interaction.guild.categories, name="Teams")
#             text_channel = await interaction.guild.create_text_channel(
#                 team_name, category=category
#             )
#             voice_channel = await interaction.guild.create_voice_channel(
#                 team_name, category=category
#             )
#             for hacker in team:
#                 user = interaction.guild.get_member_named(hacker["username"])
#                 await text_channel.set_permissions(user, read_messages=True)
#                 await voice_channel.set_permissions(user, view_channel=True)

#     except Exception as e:
#         logging.error(
#             f"start_random_matchmaking: Error starting random matchmaking {interaction.user}: {e}"
#         )
#         await interaction.response.send_message(
#             "An error occurred while starting random matchmaking.", ephemeral=True
#         )
#         return


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
