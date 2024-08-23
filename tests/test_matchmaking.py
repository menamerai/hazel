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


def test_calculate_compatibility(hacker1, hacker2):
    assert calculate_compatibility(hacker1, hacker2) - 77.72998611746911 < 0.0001


def test_matchmake(hacker_group):
    random.seed(0)
    random.shuffle(hacker_group)
    groups = matchmake(hacker_group)
    assert len(groups) == 14


def test_matchmake_on_single_hacker(hacker1):
    groups = matchmake([hacker1])
    assert len(groups) == 1
    assert len(groups[0]) == 1
    assert groups[0][0] == hacker1


def test_matchmake_two_roots_with_single_hacker(hacker1, hacker3):
    groups = matchmake([hacker1, hacker3])
    assert len(groups) == 2
    assert len(groups[0]) == 1
    assert len(groups[1]) == 1
    assert groups[0][0] == hacker1
    assert groups[1][0] == hacker3


def test_matchmake_on_empty_group():
    groups = matchmake([])
    assert len(groups) == 0


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
