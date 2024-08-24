import logging
import random

import discord
from discord import app_commands
from supabase import Client

from hazel.services.supabase_client import supabase_client
from hazel.utils.channels import random_channel_name
from hazel.utils.compatibility import match_mentor_team, matchmake
from hazel.utils.models import *


class Matchmake(app_commands.Group):
    @app_commands.command(description="Start matchmaking for hackers (Admin only)")
    @app_commands.checks.has_role("Admin")
    async def hacker(self, interaction: discord.Interaction, seed: int = 42):
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

            await supabase.table("team").insert(
                {
                    "root": root,
                    "leaf": leaf,
                    "branch": branch,
                    "members": members,
                    "leader": members[0],
                    "matchmade": True,
                }
            ).execute()
            await supabase.table("hacker").update(
                {"has_team": True, "matchmade": True}
            ).in_("username", members).execute()
            # TODO: create a channel for the team (?)
            logging.info(f"Matchmake.start: Saved group {members} to the database")

        await interaction.followup.send("Matchmaking complete!", ephemeral=True)

    @hacker.error
    async def hacker_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CheckFailure):
            await interaction.response.send_message(
                "You do not have permission to use this command", ephemeral=True
            )

    @app_commands.command(
        description="Create channels for matchmade teams (Admin only)"
    )
    @app_commands.checks.has_role("Admin")
    async def create_matchmade_channels(self, interaction: discord.Interaction):
        logging.info(
            f"Matchmake.create_channels: Received create channels request from {interaction.user}"
        )
        await interaction.response.defer(ephemeral=True)

        supabase: Client = self.extras["supabase"]

        # Get all teams that have been matchmade
        teams = (
            supabase.table("team").select("members").is_("matchmade", True).execute()
        )
        if hasattr(teams, "data"):
            teams = teams.data
            logging.info(
                f"Matchmake.create_channels: Found {len(teams)} teams in the database"
            )
        else:
            await interaction.followup.send(
                "No teams found in the database", ephemeral=True
            )
            return

        members = [team["members"] for team in teams[0]]
        # Create channels for the teams
        for team in teams:
            channel_name = random_channel_name()
            try:
                # create a text channel for the team and overwrite the permissions to only allow the team members to view it
                members_obj = [
                    discord.utils.get(interaction.guild.members, name=member)
                    for member in members
                ]
                await interaction.guild.create_text_channel(
                    name=channel_name,
                    category=discord.utils.get(
                        interaction.guild.categories, name="Teams"
                    ),
                    overwrites={
                        interaction.guild.default_role: discord.PermissionOverwrite(
                            read_messages=False
                        ),
                        interaction.guild.me: discord.PermissionOverwrite(
                            read_messages=True
                        ),
                        interaction.user: discord.PermissionOverwrite(
                            read_messages=True
                        ),
                        **{
                            member: discord.PermissionOverwrite(read_messages=True)
                            for member in members_obj
                        },
                    },
                )
                logging.info(
                    f"Matchmake.create_channels: Created channel {channel_name} for team {team.members}"
                )
            except Exception as e:
                logging.error(
                    f"Matchmake.create_channels: Error creating channel for team {team.members}"
                )
                logging.error(e)

        await interaction.followup.send("Channels created!", ephemeral=True)

    @app_commands.command(description="Start matchmaking for mentors (Admin only)")
    @app_commands.checks.has_role("Admin")
    async def mentor(self, interaction: discord.Interaction, seed: int = 42):
        logging.info(f"Matchmake.start: Received start request from {interaction.user}")
        await interaction.response.defer(ephemeral=True)

        supabase: Client = self.extras["supabase"]

        # Get all mentors in the database
        mentors = supabase.table("mentor").select("*").execute()
        if hasattr(mentors, "data"):
            mentors = mentors.data
            logging.info(
                f"Matchmake.start: Found {len(mentors)} mentors in the database"
            )
        else:
            await interaction.followup.send(
                "No mentors found in the database", ephemeral=True
            )
            return

        # Convert the mentors to Mentor objects
        mentors = [
            Mentor(
                username=mentor["username"],
                root=Root(mentor["root"]),
                branch=Branch(mentor["branch"]),
            )
            for mentor in mentors
        ]
        logging.info(f"Matchmake.start: Converted mentors to {mentors} objects")
        # Shuffle the mentors to make the matchmaking process random
        random.seed(seed)
        random.shuffle(mentors)
        # Get all teams in the database
        teams = supabase.table("team").select("*").execute()
        if hasattr(teams, "data"):
            teams = teams.data
            logging.info(f"Matchmake.start: Found {len(teams)} teams in the database")
        else:
            await interaction.followup.send(
                "No teams found in the database", ephemeral=True
            )
            return

        # Convert the teams to Team objects
        teams = [
            Team(
                root=Root(team["root"]),
                branch=Branch(team["branch"]),
                members=team["members"],
                leader=team["leader"],
            )
            for team in teams
        ]
        logging.info(f"Matchmake.start: Converted teams to {teams} objects")
        # Matchmake the mentors to the teams
        mentor_teams, unmatched_teams = match_mentor_team(mentors, teams)
        logging.info(
            f"Matchmake.start: Matchmaking complete. Found {len(mentor_teams)} mentor teams"
        )
        # Save the mentor teams to the database
        for mentor, teams in mentor_teams.items():
            for team in teams:
                try:
                    await supabase.table("team").update(
                        {"mentor": mentor.username}
                    ).in_("leader", team.members).execute()
                    # increment the mentor's team count
                    team_count = (
                        supabase.table("mentor")
                        .select("num_mentored_teams")
                        .eq("username", mentor.username)
                        .execute()
                        .data[0]["num_mentored_teams"]
                    )
                    await supabase.table("mentor").update(
                        {"num_mentored_teams": team_count + 1}
                    ).eq("username", mentor.username).execute()
                    logging.info(
                        f"Matchmake.start: Saved mentor {mentor.username} to team {team.members}"
                    )
                except Exception as e:
                    logging.error(
                        f"Matchmake.start: Error saving mentor {mentor.username} to team {team.members}"
                    )
                    logging.error(e)

        # Save the unmatched teams to the database
        for team in unmatched_teams:
            try:
                await supabase.table("team").update({"mentor": "<UNMATCHED>"}).in_(
                    "leader", team.members
                ).execute()
                logging.info(
                    f"Matchmake.start: Saved mentor unmatched to team {team.members}"
                )
            except Exception as e:
                logging.error(
                    f"Matchmake.start: Error saving mentor unmatched to team {team.members}"
                )
                logging.error(e)

        await interaction.followup.send("Matchmaking complete!", ephemeral=True)

    @mentor.error
    async def mentor_error(self, interaction: discord.Interaction, error):
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
