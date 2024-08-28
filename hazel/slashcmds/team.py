import logging
import re
from datetime import datetime

import discord
from discord import app_commands
from dotenv import load_dotenv
from supabase import Client

from hazel.services.supabase_client import supabase_client
from hazel.utils.constants import *
from hazel.utils.users import check_if_user_exists


async def create_team(
    interaction: discord.Interaction,
    supabase: Client,
    root: str,
    branch: str,
    leaf: str,
):
    logging.info(
        f"create_team: creating team for {interaction.user} with root: {root}, branch: {branch}, and leaf: {leaf}"
    )
    supabase.table("team").insert(
        {
            "leader": interaction.user.name,
            "root": root,
            "branch": branch,
            "leaf": leaf,
            "members": [interaction.user.name],
            "matchmade": False,
        }
    ).execute()
    supabase.table("hacker").update(
        {
            "has_team": True,
        }
    ).eq("username", interaction.user.name).execute()
    logging.info(f"create_team: {interaction.user}'s team created successfully")
    await interaction.response.send_message(
        "Your team has been created.", ephemeral=True
    )


async def update_team(
    interaction: discord.Interaction,
    supabase: Client,
    root: str,
    branch: str,
    leaf: str,
):
    logging.info(
        f"update_team: updating team for {interaction.user} with root: {root}, branch: {branch}, and leaf: {leaf}"
    )
    team = (
        supabase.table("team")
        .select("id")
        .eq("leader", interaction.user.name)
        .execute()
    )
    team_id = team.data[0]["id"]
    supabase.table("team").update(
        {
            "root": root,
            "branch": branch,
            "leaf": leaf,
        }
    ).eq("id", team_id).execute()
    logging.info(f"update_team: {interaction.user}'s team updated successfully")
    await interaction.response.send_message(
        "Your team has been updated.", ephemeral=True
    )


class RootSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Software Root",
                value="software hacker",
                description="Software development, programming, and coding",
                emoji="💻",
            ),
            discord.SelectOption(
                label="Business/Creative Root",
                value="pitch competition hacker",
                description="Business, marketing, design, and creative",
                emoji="💼",
            ),
        ]
        super().__init__(
            placeholder="Select your team's root",
            options=options,
            custom_id="root",
            max_values=1,
            min_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        root = self.values[0]
        logging.info(f"RootSelect.callback: selected root: {root}")
        self.view.root = root
        self.view.root_answered = True

        if (
            self.view.root_answered
            and self.view.branch_answered
            and self.view.leaf_answered
        ):
            self.view.stop()

            if self.view.mode == "edit":
                await update_team(
                    interaction=interaction,
                    supabase=self.view.supabase,
                    root=self.view.root,
                    branch=self.view.branch,
                    leaf=self.view.leaf,
                )
            else:
                await create_team(
                    interaction=interaction,
                    supabase=self.view.supabase,
                    root=self.view.root,
                    branch=self.view.branch,
                    leaf=self.view.leaf,
                )
        else:
            await interaction.response.defer()


class BranchSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Artificial Intelligence Branch",
                value="ai track",
                description="Machine learning, deep learning, and artificial intelligence",
                emoji="🧠",
            ),
            discord.SelectOption(
                label="Blockchain Branch",
                value="blockchain track",
                description="Cryptocurrency, smart contracts, and decentralized finance",
                emoji="🟦",
            ),
            discord.SelectOption(
                label="Data Visualization Branch",
                value="data visualization track",
                description="Data analysis, data visualization, and data science",
                emoji="📊",
            ),
        ]
        super().__init__(
            placeholder="Select your team's branch",
            options=options,
            custom_id="branch",
            max_values=1,
            min_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        branch = self.values[0]
        logging.info(f"BranchSelect.callback: selected branch: {branch}")
        self.view.branch = branch
        self.view.branch_answered = True

        if (
            self.view.root_answered
            and self.view.branch_answered
            and self.view.leaf_answered
        ):
            self.view.stop()
            if self.view.mode == "edit":
                await update_team(
                    interaction=interaction,
                    supabase=self.view.supabase,
                    root=self.view.root,
                    branch=self.view.branch,
                    leaf=self.view.leaf,
                )
            else:
                await create_team(
                    interaction=interaction,
                    supabase=self.view.supabase,
                    root=self.view.root,
                    branch=self.view.branch,
                    leaf=self.view.leaf,
                )
        else:
            await interaction.response.defer()


class LeafSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Gaming Theme",
                value="gaming theme",
                description="Gaming, esports, and entertainment",
                emoji="🎮",
            ),
            discord.SelectOption(
                label="Security Theme",
                value="security theme",
                description="Cybersecurity, privacy, and digital rights",
                emoji="🛡",
            ),
            discord.SelectOption(
                label="Finance Theme",
                value="finance theme",
                description="Finance, fintech, and blockchain",
                emoji="🏧",
            ),
            discord.SelectOption(
                label="Social Impact Theme",
                value="social impact theme",
                description="Social impact, sustainability, and community",
                emoji="🌍",
            ),
        ]
        super().__init__(
            placeholder="Select your team's leaf",
            options=options,
            custom_id="leaf",
            max_values=1,
            min_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        leaf = self.values[0]
        logging.info(f"LeafSelect.callback: selected leaf: {leaf}")
        self.view.leaf = leaf
        self.view.leaf_answered = True

        if (
            self.view.root_answered
            and self.view.branch_answered
            and self.view.leaf_answered
        ):
            self.view.stop()
            if self.view.mode == "edit":
                await update_team(
                    interaction=interaction,
                    supabase=self.view.supabase,
                    root=self.view.root,
                    branch=self.view.branch,
                    leaf=self.view.leaf,
                )
            else:
                await create_team(
                    interaction=interaction,
                    supabase=self.view.supabase,
                    root=self.view.root,
                    branch=self.view.branch,
                    leaf=self.view.leaf,
                )
        else:
            await interaction.response.defer()


class TeamCreate(discord.ui.View):
    def __init__(self, supabase: Client, mode: str = "create"):
        super().__init__(timeout=3000)
        self.supabase = supabase
        self.mode = mode
        self.original_interaction: discord.Interaction | None = None
        self.root: str = "software hacker"
        self.branch: str = "ai track"
        self.leaf: str = "social impact theme"
        self.root_answered = False
        self.branch_answered = False
        self.leaf_answered = False
        self.add_item(RootSelect())
        self.add_item(BranchSelect())
        self.add_item(LeafSelect())


class Team(app_commands.Group):
    @app_commands.command(description="Register as a hacker for the event")
    async def create(self, interaction: discord.Interaction):
        logging.info(
            f"Team.create: received team creation request from {interaction.user}"
        )
        supabase: Client = self.extras["supabase"]

        # defer the response to avoid timeout
        await interaction.response.defer(ephemeral=True)

        # check if it is currently 8AM August 24th 2024
        if datetime.now() < datetime(2024, 8, 24, 8, 0, 0):
            logging.warning(
                f"Team.create: {interaction.user} tried to create a team before the event started"
            )
            await interaction.followup.send(
                "The event has not started yet. Please try again later.", ephemeral=True
            )
            return

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase,
            username=interaction.user.name,
            table="hacker",
        ):
            logging.warning(
                f"Team.create: {interaction.user} has not registered for the event"
            )
            await interaction.followup.send(
                "You haven't registered for the event. Please do so with `/register hacker`",
                ephemeral=True,
            )
            return

        # check if user is already in a team
        in_team = (
            supabase.table("hacker")
            .select("has_team")
            .eq("username", interaction.user.name)
            .execute()
            .data[0]["has_team"]
        )
        if in_team:
            logging.warning(f"Team.create: {interaction.user} is already in a team")
            await interaction.followup.send(
                "You are already in a team. You can only create a team if you are not in a team.",
                ephemeral=True,
            )
            return

        # create team
        logging.info(f"Team.create: creating team for {interaction.user}")
        try:
            view = TeamCreate(supabase=supabase)
            await interaction.followup.send(
                "Select your team's root, branch, and leaf",
                view=view,
                ephemeral=True,
            )

        except Exception as e:
            logging.error(
                f"Team.create: error while creating team for {interaction.user}: {e}"
            )
            await interaction.followup.send(
                "An error occurred while creating your team. Please try again later.",
                ephemeral=True,
            )

    @app_commands.command(description="Edit your team's root, branch, and leaf")
    async def edit(self, interaction: discord.Interaction):
        logging.info(f"Team.edit: received team edit request from {interaction.user}")
        supabase: Client = self.extras["supabase"]

        # defer the response to avoid timeout
        await interaction.response.defer(ephemeral=True)

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase,
            username=interaction.user.name,
            table="hacker",
        ):
            logging.warning(
                f"Team.edit: {interaction.user} has not registered for the event"
            )
            await interaction.followup.send(
                "You haven't registered for the event. Please do so with `/register hacker`",
                ephemeral=True,
            )
            return

        # check if user is leader of a team
        team = (
            supabase.table("team")
            .select("id", count="exact")
            .eq("leader", interaction.user.name)
            .execute()
        )
        if hasattr(team, "count") and team.count == 0:
            logging.warning(f"Team.edit: {interaction.user} has not created a team")
            await interaction.followup.send(
                "You are not the leader of a team. You can only edit a team that you are leader of.",
                ephemeral=True,
            )
            return

        # edit team
        logging.info(f"Team.edit: editing team for {interaction.user}")
        try:
            view = TeamCreate(supabase=supabase, mode="edit")
            await interaction.followup.send(
                "Select your team's root, branch, and leaf",
                view=view,
                ephemeral=True,
            )

        except Exception as e:
            logging.error(
                f"Team.edit: error while editing team for {interaction.user}: {e}"
            )
            await interaction.followup.send(
                "An error occurred while editing your team. Please try again later.",
                ephemeral=True,
            )

    @app_commands.command(description="Disband your team")
    async def disband(self, interaction: discord.Interaction):
        logging.info(
            f"Team.disband: received team disband request from {interaction.user}"
        )
        supabase: Client = self.extras["supabase"]

        # defer the response to avoid timeout
        await interaction.response.defer(ephemeral=True)

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase,
            username=interaction.user.name,
            table="hacker",
        ):
            logging.warning(
                f"Team.disband: {interaction.user} has not registered for the event"
            )
            await interaction.followup.send(
                "You haven't registered for the event. Please do so with `/register hacker`",
                ephemeral=True,
            )
            return

        # check if user is leader of a team
        team = (
            supabase.table("team")
            .select("id", count="exact")
            .eq("leader", interaction.user.name)
            .execute()
        )
        if hasattr(team, "count") and team.count == 0:
            logging.warning(
                f"Team.disband: {interaction.user} is not a leader of a team"
            )
            await interaction.followup.send(
                "You are not a leader of a team. You can only disband a team that you are leader of.",
                ephemeral=True,
            )
            return

        # delete team
        logging.info(f"Team.disband: deleting team for {interaction.user}")
        try:
            members = (
                supabase.table("team")
                .select("members")
                .eq("leader", interaction.user.name)
                .execute()
                .data[0]["members"]
            )
            supabase.table("team").delete().eq(
                "leader", interaction.user.name
            ).execute()
            for member in members:
                supabase.table("hacker").update(
                    {
                        "has_team": False,
                    }
                ).eq("username", member).execute()
            logging.info(
                f"Team.disband: {interaction.user}'s team disbanded successfully"
            )
            await interaction.followup.send(
                "Your team has been disbanded.", ephemeral=True
            )

        except Exception as e:
            logging.error(
                f"Team.disband: error while deleting team for {interaction.user}: {e}"
            )
            await interaction.followup.send(
                "An error occurred while disbanding your team. Please try again later.",
                ephemeral=True,
            )

    @app_commands.command(description="Add a member to your team")
    async def add(self, interaction: discord.Interaction, user: str):
        logging.info(f"Team.add: received team add request from {interaction.user}")
        supabase: Client = self.extras["supabase"]

        # defer the response to avoid timeout
        await interaction.response.defer(ephemeral=True)

        # check if user instead inputting a username, inputted a mention
        if re.match(r"<@!?(\d+)>", user):
            user = interaction.guild.get_member(int(user[2:-1])).name

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase,
            username=interaction.user.name,
            table="hacker",
        ):
            logging.warning(
                f"Team.add: {interaction.user} has not registered for the event"
            )
            await interaction.followup.send(
                "You haven't registered for the event. Please do so with `/register hacker`",
                ephemeral=True,
            )
            return

        # Check if user being added exists in the database
        if not check_if_user_exists(
            client=supabase,
            username=user,
            table="hacker",
        ):
            logging.warning(f"Team.add: {user} has not registered for the event")
            await interaction.followup.send(
                f"{user} hasn't registered for the event. Please ask them to register with `/register hacker`",
                ephemeral=True,
            )
            return

        # check if user is leader of a team
        team = (
            supabase.table("team")
            .select("id", count="exact")
            .eq("leader", interaction.user.name)
            .execute()
        )
        if hasattr(team, "count") and team.count == 0:
            logging.warning(f"Team.add: {interaction.user} is not a leader of a team")
            await interaction.followup.send(
                "You are not a leader of a team. You can only add a member to a team that you are leader of.",
                ephemeral=True,
            )
            return

        # check if user being added is already in a team
        in_team = (
            supabase.table("hacker")
            .select("has_team")
            .eq("username", user)
            .execute()
            .data[0]["has_team"]
        )
        if in_team:
            logging.warning(f"Team.add: {user} is already in a team")
            await interaction.followup.send(
                f"{user} is already in a team. You can only add a user who is not in a team.",
                ephemeral=True,
            )
            return

        # check if team is full
        members = (
            supabase.table("team")
            .select("members")
            .limit(1)
            .eq("leader", interaction.user.name)
            .execute()
        )
        if len(members.data[0]["members"]) >= 4:
            logging.warning(f"Team.add: {interaction.user}'s team is full")
            await interaction.followup.send(
                "Your team is full. You can only add a member if your team has less than 4 members.",
                ephemeral=True,
            )
            return

        # add member to team
        logging.info(f"Team.add: adding {user} to {interaction.user}'s team")
        try:
            logging.info(f"Team.add: current members: {members.data[0]['members']}")
            supabase.table("team").update(
                {
                    "members": [user] + members.data[0]["members"],
                }
            ).eq("leader", interaction.user.name).execute()
            supabase.table("hacker").update(
                {
                    "has_team": True,
                }
            ).eq("username", user).execute()
            logging.info(
                f"Team.add: {user} added to {interaction.user}'s team successfully"
            )
            await interaction.followup.send(
                f"{user} has been added to your team.", ephemeral=True
            )

        except Exception as e:
            logging.error(
                f"Team.add: error while adding {user} to {interaction.user}'s team: {e}"
            )
            await interaction.followup.send(
                f"An error occurred while adding {user} to your team. Please try again later.",
                ephemeral=True,
            )

    @app_commands.command(description="Remove a member from your team")
    async def remove(self, interaction: discord.Interaction, user: str):
        logging.info(
            f"Team.remove: received team remove request from {interaction.user}"
        )
        supabase: Client = self.extras["supabase"]

        # defer the response to avoid timeout
        await interaction.response.defer(ephemeral=True)

        # check if user instead inputting a username, inputted a mention
        if re.match(r"<@!?(\d+)>", user):
            user = interaction.guild.get_member(int(user[2:-1])).name

        # check if the person being removed is the leader
        if interaction.user.name == user:
            logging.warning(
                f"Team.remove: {interaction.user} tried to remove themselves"
            )
            await interaction.followup.send(
                "You cannot remove yourself from the team. Use `/team leave` to leave the team.",
                ephemeral=True,
            )
            return

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase,
            username=interaction.user.name,
            table="hacker",
        ):
            logging.warning(
                f"Team.remove: {interaction.user} has not registered for the event"
            )
            await interaction.followup.send(
                "You haven't registered for the event. Please do so with `/register hacker`",
                ephemeral=True,
            )
            return

        # Check if user being removed exists in the database
        if not check_if_user_exists(
            client=supabase,
            username=user,
            table="hacker",
        ):
            logging.warning(f"Team.remove: cannot find {user} in the database")
            await interaction.followup.send(
                f"Cannot find {user} in the database.", ephemeral=True
            )
            return

        # check if user is leader of a team
        in_team = (
            supabase.table("team")
            .select("leader")
            .eq("leader", interaction.user.name)
            .execute()
            .data[0]["leader"]
        )
        if not in_team:
            logging.warning(
                f"Team.remove: {interaction.user} is not a leader of a team"
            )
            await interaction.followup.send(
                "You are not a leader of a team. You can only remove a member from a team that you are leader of.",
                ephemeral=True,
            )
            return

        # check if user being removed is part of your team
        members = (
            supabase.table("team")
            .select("members")
            .limit(1)
            .eq("leader", interaction.user.name)
            .execute()
        )
        if user not in members.data[0]["members"]:
            logging.warning(f"Team.remove: {user} is not in {interaction.user}'s team")
            await interaction.followup.send(
                f"{user} is not in your team. You can only remove a member who is in your team.",
                ephemeral=True,
            )
            return

        # remove member from team
        logging.info(f"Team.remove: removing {user} from {interaction.user}'s team")
        try:
            members = members.data[0]
            logging.info(f"Team.remove: current members: {members}")
            members.remove(user)
            supabase.table("team").update(
                {
                    "members": members,
                }
            ).eq("leader", interaction.user.name).execute()
            supabase.table("hacker").update(
                {
                    "has_team": False,
                }
            ).eq("username", user).execute()
            logging.info(
                f"Team.remove: {user} removed from {interaction.user}'s team successfully"
            )
            await interaction.followup.send(
                f"{user} has been removed from your team.", ephemeral=True
            )

        except Exception as e:
            logging.error(
                f"Team.remove: error while removing {user} from {interaction.user}'s team: {e}"
            )
            await interaction.followup.send(
                f"An error occurred while removing {user} from your team. Please try again later.",
                ephemeral=True,
            )

    @app_commands.command(description="Leave your team")
    async def leave(self, interaction: discord.Interaction):
        logging.info(f"Team.leave: received team leave request from {interaction.user}")
        supabase: Client = self.extras["supabase"]

        # defer the response to avoid timeout
        await interaction.response.defer(ephemeral=True)

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase,
            username=interaction.user.name,
            table="hacker",
        ):
            logging.warning(
                f"Team.leave: {interaction.user} has not registered for the event"
            )
            await interaction.followup.send(
                "You haven't registered for the event. Please do so with `/register hacker`",
                ephemeral=True,
            )
            return

        # check if user is in a team
        in_team = (
            supabase.table("hacker")
            .select("has_team")
            .eq("username", interaction.user.name)
            .execute()
            .data[0]["has_team"]
        )
        if not in_team:
            logging.warning(f"Team.leave: {interaction.user} is not in a team")
            await interaction.followup.send(
                "You are not in a team. You can only leave a team if you are in a team.",
                ephemeral=True,
            )
            return

        # check if user is a leader of a team
        leader = (
            supabase.table("team")
            .select("leader", count="exact")
            .limit(1)
            .eq("leader", interaction.user.name)
            .execute()
        )
        if hasattr(leader, "count") and leader.count == 1:
            logging.warning(f"Team.leave: {interaction.user} is a leader of a team")
            await interaction.followup.send(
                "You are a leader of a team. You can only leave a team if you are not a leader of a team. Use `/team disband` to disband your team, or `/team transfer_leader` to transfer leadership to another member.",
                ephemeral=True,
            )
            return

        # leave team
        logging.info(f"Team.leave: leaving team for {interaction.user}")
        try:
            members = (
                supabase.table("team")
                .select("members")
                .limit(1)
                .eq("leader", interaction.user.name)
                .execute()
            ).data[0]["members"]
            logging.info(f"Team.leave: current members: {members}")
            members.remove(interaction.user.name)
            supabase.table("team").update(
                {
                    "members": members,
                }
            ).eq("leader", interaction.user.name).execute()
            supabase.table("hacker").update(
                {
                    "has_team": False,
                }
            ).eq("username", interaction.user.name).execute()
            logging.info(f"Team.leave: {interaction.user} left the team successfully")
            await interaction.followup.send("You have left the team.", ephemeral=True)

        except Exception as e:
            logging.error(
                f"Team.leave: error while leaving team for {interaction.user}: {e}"
            )
            await interaction.followup.send(
                "An error occurred while leaving the team. Please try again later.",
                ephemeral=True,
            )

    @app_commands.command(description="Transfer leadership of your team")
    async def transfer_leader(self, interaction: discord.Interaction, user: str):
        logging.info(
            f"Team.transfer_leader: received team transfer leadership request from {interaction.user}"
        )
        supabase: Client = self.extras["supabase"]

        await interaction.response.defer(ephemeral=True)

        # check if user instead inputting a username, inputted a mention
        if re.match(r"<@!?(\d+)>", user):
            user = interaction.guild.get_member(int(user[2:-1])).name

        # check if the person being transferred leadership is the leader
        if interaction.user.name == user:
            logging.warning(
                f"Team.transfer_leader: {interaction.user} tried to transfer leadership to themselves"
            )
            await interaction.followup.send(
                "You cannot transfer leadership to yourself.",
                ephemeral=True,
            )
            return

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase,
            username=interaction.user.name,
            table="hacker",
        ):
            logging.warning(
                f"Team.transfer_leader: {interaction.user} has not registered for the event"
            )
            await interaction.followup.send(
                "You haven't registered for the event. Please do so with `/register hacker`",
                ephemeral=True,
            )
            return

        # Check if user being transferred leadership exists in the database
        if not check_if_user_exists(
            client=supabase,
            username=user,
            table="hacker",
        ):
            logging.warning(f"Team.transfer_leader: cannot find {user} in the database")
            await interaction.followup.send(
                f"Cannot find {user} in the database.", ephemeral=True
            )
            return

        # check if user is leader of a team
        leader = (
            supabase.table("team")
            .select("leader", count="exact")
            .eq("leader", interaction.user.name)
            .execute()
        )
        if hasattr(leader, "count") and leader.count == 0:
            logging.warning(
                f"Team.transfer_leader: {interaction.user} is not a leader of a team"
            )
            await interaction.followup.send(
                "You are not a leader of a team. You can only transfer leadership if you are a leader of a team.",
                ephemeral=True,
            )
            return

        # check if user being transferred leadership is not part of the team
        members = (
            supabase.table("team")
            .select("members")
            .limit(1)
            .eq("leader", interaction.user.name)
            .execute()
        )
        if user not in members.data[0]["members"]:
            logging.warning(
                f"Team.transfer_leader: {user} is not in {interaction.user}'s team"
            )
            await interaction.followup.send(
                f"{user} is not in your team. You can only transfer leadership to a member who is in your team.",
                ephemeral=True,
            )
            return

        # transfer leadership
        logging.info(
            f"Team.transfer_leader: transferring leadership from {interaction.user} to {user}"
        )
        try:
            supabase.table("team").update(
                {
                    "leader": user,
                }
            ).eq("leader", interaction.user.name).execute()
            logging.info(
                f"Team.transfer_leader: leadership transferred from {interaction.user} to {user} successfully"
            )
            await interaction.followup.send(
                f"Leadership has been transferred to {user}.", ephemeral=True
            )

        except Exception as e:
            logging.error(
                f"Team.transfer_leader: error while transferring leadership from {interaction.user} to {user}: {e}"
            )
            await interaction.followup.send(
                f"An error occurred while transferring leadership to {user}. Please try again later.",
                ephemeral=True,
            )

    @app_commands.command(description="View your team")
    async def view(self, interaction: discord.Interaction):
        logging.info(f"Team.view: received team view request from {interaction.user}")
        supabase: Client = self.extras["supabase"]

        # defer the response to avoid timeout
        await interaction.response.defer(ephemeral=True)

        # Check if user exists in the database
        if not check_if_user_exists(
            client=supabase,
            username=interaction.user.name,
            table="hacker",
        ):
            logging.warning(
                f"Team.view: {interaction.user} has not registered for the event"
            )
            await interaction.followup.send(
                "You haven't registered for the event. Please do so with `/register hacker`",
                ephemeral=True,
            )
            return

        # check if user is in a team
        has_team = (
            supabase.table("hacker")
            .select("has_team")
            .eq("username", interaction.user.name)
            .execute()
            .data[0]["has_team"]
        )
        if not has_team:
            logging.warning(f"Team.view: {interaction.user} is not in a team")
            await interaction.followup.send(
                "You are not in a team. You can only view a team if you are in a team.",
                ephemeral=True,
            )
            return

        # view team
        logging.info(f"Team.view: viewing team for {interaction.user}")
        try:
            team = (
                supabase.table("team")
                .select("leader, root, branch, leaf, members, mentor, mentor_email")
                .limit(1)
                .contains("members", [interaction.user.name])
                .execute()
            ).data[0]

            team_embed = discord.Embed(
                title=f"Leader: {team['leader']}",
                description=f"Root: {team['root']}\nBranch: {team['branch']}\nLeaf: {team['leaf']}",
                color=discord.Color.blue(),
            )
            team_embed.add_field(
                name="Mentor",
                value=f"Discord ID: {team['mentor'] if 'mentor' in team else 'None'}\nEmail: {team['mentor_email'] if 'mentor_email' in team else 'None'}",
            )
            team_embed.add_field(name="Members", value="\n".join(team["members"]))
            await interaction.followup.send(embed=team_embed, ephemeral=True)

        except Exception as e:
            logging.error(
                f"Team.view: error while viewing team for {interaction.user}: {e}"
            )
            await interaction.followup.send(
                "An error occurred while viewing the team. Please try again later.",
                ephemeral=True,
            )


async def setup(client: discord.Client):
    logging.info("Team: registering slash command")
    load_dotenv()
    client.tree.add_command(
        Team(
            name="team",
            description="Start and manage your team for mentor matching",
            extras={
                "supabase": supabase_client,
            },
        )
    )
