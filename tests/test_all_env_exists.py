import os

from dotenv import load_dotenv


def test_all_env_exists():
    load_dotenv()
    assert os.getenv("HAZEL_TOKEN")
    assert os.getenv("FODH_GUILD_ID")
