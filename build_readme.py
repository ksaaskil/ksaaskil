"""
Inspired by and some of the code copied from
https://github.com/simonw/simonw/blob/main/build_readme.py
"""
from datetime import datetime, timezone
import pathlib
import os
import re

from python_graphql_client import GraphqlClient


root = pathlib.Path(__file__).parent.resolve()
client = GraphqlClient(endpoint="https://api.github.com/graphql")

TOKEN = os.environ.get("API_TOKEN", "")


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


if __name__ == "__main__":
    readme = root / "README.md"

    readme_content = readme.open("r").read()

    updated_at_md = "Updated at {date}.".format(
        date=datetime.now(timezone.utc).isoformat()
    )

    rewritten = replace_chunk(readme_content, "updated_at", updated_at_md)

    readme.open("w").write(rewritten)
