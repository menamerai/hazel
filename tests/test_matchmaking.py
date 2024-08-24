import json
import random

import pytest

from hazel.utils.compatibility import *


@pytest.fixture
def hacker1():
    return Hacker("hacker1", Root.SOFTWARE, Leaf.GAMING, Branch.AI)


@pytest.fixture
def hacker2():
    return Hacker("hacker2", Root.SOFTWARE, Leaf.GAMING, Branch.AI)


@pytest.fixture
def hacker3():
    return Hacker("hacker3", Root.PITCH, Leaf.GAMING, Branch.AI)


@pytest.fixture
def three_non_matching_hackers_in_same_root():
    return [
        Hacker("hacker1", Root.SOFTWARE, Leaf.GAMING, Branch.AI),
        Hacker("hacker2", Root.SOFTWARE, Leaf.SECURITY, Branch.BLOCKCHAIN),
        Hacker("hacker3", Root.SOFTWARE, Leaf.FINANCE, Branch.DATA),
    ]


@pytest.fixture
def hacker_group():
    return [
        Hacker("Alice", Root.SOFTWARE, Leaf.GAMING, Branch.AI),
        Hacker("Bob", Root.PITCH, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Charlie", Root.SOFTWARE, Leaf.FINANCE, Branch.DATA),
        Hacker("David", Root.PITCH, Leaf.GAMING, Branch.AI),
        Hacker("Eve", Root.SOFTWARE, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Frank", Root.PITCH, Leaf.FINANCE, Branch.DATA),
        Hacker("Grace", Root.SOFTWARE, Leaf.GAMING, Branch.AI),
        Hacker("Hank", Root.PITCH, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Ivy", Root.SOFTWARE, Leaf.FINANCE, Branch.DATA),
        Hacker("Jack", Root.PITCH, Leaf.GAMING, Branch.AI),
        Hacker("Kathy", Root.SOFTWARE, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Liam", Root.PITCH, Leaf.FINANCE, Branch.DATA),
        Hacker("Mary", Root.SOFTWARE, Leaf.GAMING, Branch.AI),
        Hacker("Nancy", Root.PITCH, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Oscar", Root.SOFTWARE, Leaf.FINANCE, Branch.DATA),
        Hacker("Peter", Root.PITCH, Leaf.GAMING, Branch.AI),
        Hacker("Quinn", Root.SOFTWARE, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Roger", Root.PITCH, Leaf.FINANCE, Branch.DATA),
        Hacker("Sally", Root.SOFTWARE, Leaf.GAMING, Branch.AI),
        Hacker("Tom", Root.PITCH, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Ursula", Root.SOFTWARE, Leaf.FINANCE, Branch.DATA),
        Hacker("Victor", Root.PITCH, Leaf.GAMING, Branch.AI),
        Hacker("Wendy", Root.SOFTWARE, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Xavier", Root.PITCH, Leaf.FINANCE, Branch.DATA),
        Hacker("Yvonne", Root.SOFTWARE, Leaf.GAMING, Branch.AI),
        Hacker("Zack", Root.PITCH, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Aaron", Root.SOFTWARE, Leaf.FINANCE, Branch.DATA),
        Hacker("Bella", Root.PITCH, Leaf.GAMING, Branch.AI),
        Hacker("Chris", Root.SOFTWARE, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Daisy", Root.PITCH, Leaf.FINANCE, Branch.DATA),
        Hacker("Ethan", Root.SOFTWARE, Leaf.GAMING, Branch.AI),
        Hacker("Fiona", Root.PITCH, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("George", Root.SOFTWARE, Leaf.FINANCE, Branch.DATA),
        Hacker("Hannah", Root.PITCH, Leaf.GAMING, Branch.AI),
        Hacker("Isaac", Root.SOFTWARE, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Jenny", Root.PITCH, Leaf.FINANCE, Branch.DATA),
        Hacker("Kevin", Root.SOFTWARE, Leaf.GAMING, Branch.AI),
        Hacker("Lily", Root.PITCH, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Mason", Root.SOFTWARE, Leaf.FINANCE, Branch.DATA),
        Hacker("Nina", Root.PITCH, Leaf.GAMING, Branch.AI),
        Hacker("Oliver", Root.SOFTWARE, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Penny", Root.PITCH, Leaf.FINANCE, Branch.DATA),
        Hacker("Quentin", Root.SOFTWARE, Leaf.GAMING, Branch.AI),
        Hacker("Rose", Root.PITCH, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Sam", Root.SOFTWARE, Leaf.FINANCE, Branch.DATA),
        Hacker("Tina", Root.PITCH, Leaf.GAMING, Branch.AI),
        Hacker("Ulysses", Root.SOFTWARE, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Violet", Root.PITCH, Leaf.FINANCE, Branch.DATA),
        Hacker("Will", Root.SOFTWARE, Leaf.GAMING, Branch.AI),
        Hacker("Xena", Root.PITCH, Leaf.SOCIAL, Branch.BLOCKCHAIN),
        Hacker("Yara", Root.SOFTWARE, Leaf.FINANCE, Branch.DATA),
        Hacker("Zane", Root.PITCH, Leaf.GAMING, Branch.AI),
    ]


@pytest.fixture
def single_team1():
    return Team(Root.SOFTWARE, Branch.AI, ["Alice", "Bob", "Charlie"], "Alice")


@pytest.fixture
def single_team2():
    return Team(Root.SOFTWARE, Branch.AI, ["Alice", "Bob", "Charlie"], "Alice")


@pytest.fixture
def single_team3():
    return Team(Root.PITCH, Branch.AI, ["Alice", "Bob", "Charlie"], "Alice")


@pytest.fixture
def three_teams():
    return [
        Team(Root.SOFTWARE, Branch.AI, ["Alice", "Bob", "Charlie"], "Alice"),
        Team(Root.SOFTWARE, Branch.BLOCKCHAIN, ["David", "Eve", "Frank"], "David"),
        Team(Root.PITCH, Branch.DATA, ["Grace", "Hank", "Ivy"], "Grace"),
    ]


@pytest.fixture
def many_teams():
    return [
        Team(Root.SOFTWARE, Branch.AI, ["Alice", "Bob", "Charlie"], "Alice"),
        Team(Root.SOFTWARE, Branch.BLOCKCHAIN, ["David", "Eve", "Frank"], "David"),
        Team(Root.PITCH, Branch.DATA, ["Grace", "Hank", "Ivy"], "Grace"),
        Team(Root.SOFTWARE, Branch.DATA, ["Jack", "Kathy", "Liam"], "Jack"),
        Team(Root.SOFTWARE, Branch.DATA, ["Mary", "Nancy", "Oscar"], "Mary"),
        Team(Root.PITCH, Branch.BLOCKCHAIN, ["Peter", "Quinn", "Roger"], "Peter"),
        Team(Root.SOFTWARE, Branch.AI, ["Sally", "Tom", "Ursula"], "Sally"),
        Team(Root.SOFTWARE, Branch.BLOCKCHAIN, ["Victor", "Wendy", "Xavier"], "Victor"),
        Team(Root.PITCH, Branch.AI, ["Yvonne", "Zack", "Aaron"], "Yvonne"),
        Team(Root.SOFTWARE, Branch.AI, ["Bella", "Chris", "Daisy"], "Bella"),
        Team(Root.SOFTWARE, Branch.BLOCKCHAIN, ["Ethan", "Fiona", "George"], "Ethan"),
        Team(Root.PITCH, Branch.AI, ["Hannah", "Isaac", "Jenny"], "Hannah"),
        Team(Root.SOFTWARE, Branch.AI, ["Kevin", "Lily", "Mason"], "Kevin"),
        Team(Root.SOFTWARE, Branch.BLOCKCHAIN, ["Nina", "Oliver", "Penny"], "Nina"),
        Team(Root.PITCH, Branch.AI, ["Quentin", "Rose", "Sam"], "Quentin"),
        Team(Root.SOFTWARE, Branch.AI, ["Tina", "Ulysses", "Violet"], "Tina"),
    ]


@pytest.fixture
def mentor1():
    return Mentor("mentor1", Root.SOFTWARE, Branch.AI)


@pytest.fixture
def mentor2():
    return Mentor("mentor2", Root.PITCH, Branch.AI)


@pytest.fixture
def mentor3():
    return Mentor("mentor3", Root.SOFTWARE, Branch.BLOCKCHAIN)


@pytest.fixture
def three_mentors():
    return [
        Mentor("mentor1", Root.SOFTWARE, Branch.AI),
        Mentor("mentor2", Root.PITCH, Branch.AI),
        Mentor("mentor3", Root.SOFTWARE, Branch.BLOCKCHAIN),
    ]


def test_calculate_hacker_compatibility(hacker1, hacker2):
    assert calculate_hacker_compatibility(hacker1, hacker2) - 77.72998611746911 < 0.0001


def test_calculate_mentor_team_compatibility(mentor1, single_team1):
    assert (
        calculate_mentor_team_compatibility(mentor1, single_team1) - 73.1058578630005
        < 0.0001
    )


def test_matchmake(hacker_group):
    random.seed(0)
    random.shuffle(hacker_group)
    groups = matchmake(hacker_group)
    assert len(groups) == 14


def test_matchmake_all_mentors_and_teams(three_mentors, many_teams):
    groups, unmatched = match_mentor_team(three_mentors, many_teams)
    assert len(groups) == 3
    assert len(groups[three_mentors[0].username]) == 4
    assert len(groups[three_mentors[1].username]) == 4
    assert len(groups[three_mentors[2].username]) == 4
    assert len(unmatched) == 4


def test_mentor_team_matchmake(
    mentor1, mentor2, mentor3, single_team1, single_team2, single_team3
):
    groups, unmatched = match_mentor_team(
        [mentor1, mentor2, mentor3], [single_team1, single_team2, single_team3]
    )
    assert len(groups[mentor1.username]) == 1
    assert len(groups[mentor2.username]) == 1
    assert len(groups[mentor3.username]) == 1
    assert len(unmatched) == 0


def test_matchmake_on_single_hacker(hacker1):
    groups = matchmake([hacker1])
    assert len(groups) == 1
    assert len(groups[0]) == 1
    assert groups[0][0] == hacker1


def test_matchmake_on_single_team(mentor1, single_team1):
    groups, _ = match_mentor_team([mentor1], [single_team1])
    assert len(groups[mentor1.username]) == 1


def test_matchmake_on_two_team_with_single_mentor(mentor1, single_team1, single_team2):
    groups, _ = match_mentor_team([mentor1], [single_team1, single_team2])
    assert len(groups[mentor1.username]) == 2


def test_matchmake_two_roots_with_single_hacker(hacker1, hacker3):
    groups = matchmake([hacker1, hacker3])
    assert len(groups) == 2
    assert len(groups[0]) == 1
    assert len(groups[1]) == 1
    assert groups[0][0] == hacker1
    assert groups[1][0] == hacker3


def test_matchmake_two_roots_with_single_team(mentor1, single_team1, single_team3):
    groups, unmatched = match_mentor_team([mentor1], [single_team1, single_team3])
    assert len(groups[mentor1.username]) == 1
    assert len(unmatched) == 1


def test_matchmake_on_empty_group():
    groups = matchmake([])
    assert len(groups) == 0


def test_matchmake_on_empty_team():
    groups, unmatched = match_mentor_team([], [])
    assert len(groups) == 0
    assert len(unmatched) == 0


def test_matchmake_on_empty_team_with_mentors(mentor1, mentor2, mentor3):
    groups, unmatched = match_mentor_team([mentor1, mentor2, mentor3], [])
    assert len(groups) == 0
    assert len(unmatched) == 0


def test_matchmake_on_single_team_with_empty_mentors(single_team1):
    groups, unmatched = match_mentor_team([], [single_team1])
    assert len(groups) == 0
    assert len(unmatched) == 1


def test_matchmake_on_three_teams_with_empty_mentors(three_teams):
    groups, unmatched = match_mentor_team([], three_teams)
    assert len(groups) == 0
    assert len(unmatched) == 3


def test_matchmake_on_odd_group(hacker1, hacker2, hacker3):
    groups = matchmake([hacker1, hacker2, hacker3])
    assert len(groups) == 2
    # one of the groups should have 2 hackers, the other should have 1
    assert len(groups[0]) == 2 or len(groups[1]) == 2
    assert len(groups[0]) == 1 or len(groups[1]) == 1


def test_matchmake_on_three_non_matching_hackers_in_same_root(
    three_non_matching_hackers_in_same_root,
):
    groups = matchmake(three_non_matching_hackers_in_same_root)
    assert len(groups) == 1
    assert len(groups[0]) == 3
