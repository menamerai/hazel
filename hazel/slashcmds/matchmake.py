import logging
import random

import discord
from discord import app_commands
from supabase import Client

from hazel.services.supabase_client import supabase_client
from hazel.utils.compatibility import matchmake
from hazel.utils.models import *


class Matchmake(app_commands.Group):
    @app_commands.command(description="Start matchmaking (Admin only)")
    @app_commands.checks.has_role("Admin")
    async def start(self, interaction: discord.Interaction, seed: int = 42):
        logging.info(f"Matchmake.start: Received start request from {interaction.user}")
        await interaction.response.defer(ephemeral=True)

        supabase: Client = self.extras["supabase"]

        # Get all hackers that are not in a team in the database
        hackers = supabase.table("hacker").select("*").is_("has_team", False).execute()
        if hasattr(hackers, "data"):
            hackers = hackers.data
            logging.info(
                f"Matchmake.start: Found {len(hackers)} hackers in the database"
            )
        else:
            await interaction.followup.send(
                "No hackers found in the database", ephemeral=True
            )
            return

        # Convert the hackers to Hacker objects
        hackers = [
            Hacker(
                username=hacker["username"],
                root=Root(hacker["root"]),
                leaf=Leaf(hacker["leaf"]),
                branch=Branch(hacker["branch"]),
            )
            for hacker in hackers
        ]
        logging.info(f"Matchmake.start: Converted hackers to {hackers} objects")
        # Shuffle the hackers to make the matchmaking process random
        random.seed(seed)
        random.shuffle(hackers)
        # Matchmake the hackers
        groups = matchmake(hackers)
        logging.info(
            f"Matchmake.start: Matchmaking complete. Found {len(groups)} groups"
        )
        # Save the groups to the database
        for group in groups:
            root = group[0].root.value
            leaf = group[0].leaf.value
            branch = group[0].branch.value
            members = [hacker.username for hacker in group]

            await supabase.table("teams").insert(
                {
                    "root": root,
                    "leaf": leaf,
                    "branch": branch,
                    "members": members,
                    "leader": members[0],
                }
            ).execute()
            await supabase.table("hackers").update({"has_team": True}).in_(
                "username", members
            ).execute()
            logging.info(f"Matchmake.start: Saved group {members} to the database")

        await interaction.followup.send("Matchmaking complete!", ephemeral=True)

    @start.error
    async def start_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CheckFailure):
            await interaction.response.send_message(
                "You do not have permission to use this command", ephemeral=True
            )


async def setup(client: discord.Client):
    logging.info("Register: registering slash command")
    client.tree.add_command(
        Matchmake(
            name="matchmake",
            description="Commands to manage matchmaking",
            extras={
                "supabase": supabase_client,
            },
        )
    )
