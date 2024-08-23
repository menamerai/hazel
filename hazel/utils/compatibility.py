import math
from itertools import combinations

from hazel.utils.models import *


def sigmoid(x: float) -> float:
    """Sigmoid function."""
    return 1 / (1 + math.exp(-x))


def calculate_compatibility(hacker1: Hacker, hacker2: Hacker) -> float:
    """Calculate the compatibility between two hackers."""
    compatibility = 0.0

    match (hacker1.root, hacker2.root):
        case (Root.SOFTWARE, Root.SOFTWARE):
            compatibility += 0.5
        case (Root.PITCH, Root.PITCH):
            compatibility += 0.5
        case (_, _):
            return compatibility

    match (hacker1.branch, hacker2.branch):
        case (Branch.AI, Branch.AI):
            compatibility += 0.5
        case (Branch.BLOCKCHAIN, Branch.BLOCKCHAIN):
            compatibility += 0.5
        case (Branch.DATA, Branch.DATA):
            compatibility += 0.5
        case (Branch.AI, Branch.BLOCKCHAIN):
            compatibility += 0.1
        case (Branch.BLOCKCHAIN, Branch.AI):
            compatibility += 0.1
        case (Branch.AI, Branch.DATA):
            compatibility += 0.375
        case (Branch.DATA, Branch.AI):
            compatibility += 0.375
        case (Branch.BLOCKCHAIN, Branch.DATA):
            compatibility += 0.25
        case (Branch.DATA, Branch.BLOCKCHAIN):
            compatibility += 0.25
        case (_, _):
            compatibility += 0.05

    match (hacker1.leaf, hacker2.leaf):
        case (Leaf.GAMING, Leaf.GAMING):
            compatibility += 0.25
        case (Leaf.SECURITY, Leaf.SECURITY):
            compatibility += 0.25
        case (Leaf.FINANCE, Leaf.FINANCE):
            compatibility += 0.25
        case (Leaf.SOCIAL, Leaf.SOCIAL):
            compatibility += 0.25
        case (Leaf.GAMING, Leaf.SECURITY):
            compatibility += 0.05
        case (Leaf.SECURITY, Leaf.GAMING):
            compatibility += 0.05
        case (Leaf.GAMING, Leaf.FINANCE):
            compatibility += 0.05
        case (Leaf.FINANCE, Leaf.GAMING):
            compatibility += 0.05
        case (Leaf.GAMING, Leaf.SOCIAL):
            compatibility += 0.15
        case (Leaf.SOCIAL, Leaf.GAMING):
            compatibility += 0.15
        case (Leaf.SECURITY, Leaf.FINANCE):
            compatibility += 0.1
        case (Leaf.FINANCE, Leaf.SECURITY):
            compatibility += 0.1
        case (Leaf.SECURITY, Leaf.SOCIAL):
            compatibility += 0.15
        case (Leaf.SOCIAL, Leaf.SECURITY):
            compatibility += 0.15
        case (Leaf.FINANCE, Leaf.SOCIAL):
            compatibility += 0.075
        case (Leaf.SOCIAL, Leaf.FINANCE):
            compatibility += 0.075
        case (_, _):
            compatibility += 0.025

    return sigmoid(compatibility) * 100


def calculate_group_compatibility(hackers: list[Hacker]) -> float:
    """Calculate the compatibility of a group of hackers."""
    if len(hackers) < 2:
        return 0.0

    compatibility = [
        calculate_compatibility(hacker1, hacker2)
        for hacker1, hacker2 in combinations(hackers, 2)
    ]
    return sum(compatibility) / len(compatibility)


def matchmake(
    hackers: list[Hacker], min_group_size: int = 2, max_group_size: int = 4
) -> list[list[Hacker]]:
    """Matchmake a list of hackers into groups. DO NOT ADD IF COMPATIBILITY IS 0.0"""

    # sort hackers by root to ensure that hackers with the same root are grouped together
    hackers_by_root = {
        root: [hacker for hacker in hackers if hacker.root == root] for root in Root
    }

    groups = []

    for _, unassigned_hackers in hackers_by_root.items():
        while unassigned_hackers:
            current_group = [unassigned_hackers.pop()]
            while len(current_group) < max_group_size and unassigned_hackers:
                best_hacker = max(
                    unassigned_hackers,
                    key=lambda h: sum(
                        calculate_compatibility(h, member) for member in current_group
                    ),
                )
                current_group.append(best_hacker)
                unassigned_hackers.remove(best_hacker)

            # if the last group is smaller than the minimum group size, distribute the remaining hackers to other groups
            if len(current_group) < min_group_size and groups:
                for hacker in current_group:
                    compatible_groups = [
                        group
                        for group in groups
                        if group[0].root == hacker.root and len(group) < max_group_size
                    ]
                    if compatible_groups:
                        best_group = max(
                            compatible_groups,
                            key=lambda g: sum(
                                calculate_compatibility(hacker, member) for member in g
                            ),
                        )
                        best_group.append(hacker)
                    else:
                        # if there are no compatible groups, create a new group
                        groups.append([hacker])
            else:
                groups.append(current_group)

    return groups
