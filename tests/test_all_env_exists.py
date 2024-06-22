import os

import pytest
from dotenv import load_dotenv


@pytest.mark.skip(reason="This can't be tested without the .env file")
def test_all_env_exists():
    load_dotenv()
    assert os.getenv("HAZEL_TOKEN")
    assert os.getenv("FODH_GUILD_ID")
