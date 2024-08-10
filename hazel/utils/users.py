from supabase import Client


def check_if_user_exists(client: Client, username: str) -> bool:
    # Check if user exists in the database
    users = (
        client.table("hacker")
        .select("id", count="exact")
        .eq("username", username)
        .execute()
    )
    if hasattr(users, "count") and users.count > 0:
        return True
    return False
