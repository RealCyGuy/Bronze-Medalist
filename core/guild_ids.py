import os

guild_ids = list(map(int, str(os.environ.get("TESTING_GUILD_ID", None)).split(","))) if os.environ.get(
    "TESTING_GUILD_ID", None) else None
