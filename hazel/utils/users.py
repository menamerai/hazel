from supabase import Client

from hazel.utils.constants import BRANCH_ROLES, LEAF_ROLES, ROOT_ROLES


def check_if_user_exists(client: Client, username: str, table: str) -> bool:
    # Check if user exists in the database
    users = (
        client.table(table)
        .select("id", count="exact")
        .eq("username", username)
        .execute()
    )
    if hasattr(users, "count") and users.count > 0:
        return True
    return False


def check_root_leaf_branch(roles: list[str]) -> bool:
    # check if there are exactly 1 root role, 1 leaf role, and 1 branch role
    root_roles = [role for role in roles if role in ROOT_ROLES]
    leaf_roles = [role for role in roles if role in LEAF_ROLES]
    branch_roles = [role for role in roles if role in BRANCH_ROLES]
    return len(root_roles) == 1 and len(leaf_roles) == 1 and len(branch_roles) == 1
