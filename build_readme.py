"""
Inspired by and some of the code copied from
https://github.com/simonw/simonw/blob/main/build_readme.py
"""
from datetime import datetime, timezone
import pathlib
import os
import re

from dotenv import load_dotenv
from gql import Client
from gql.transport.requests import RequestsHTTPTransport

load_dotenv()

root = pathlib.Path(__file__).parent.resolve()

TOKEN = os.environ.get("API_TOKEN", "")

_client: Client = None


def get_client():

    global _client

    if _client is not None:
        return _client

    sample_transport = RequestsHTTPTransport(
        url="https://api.github.com/graphql",
        use_json=True,
        headers={
            "Content-type": "application/json",
            "Authorization": f"Bearer {TOKEN}",
        },
        verify=True,
        retries=3,
    )

    _client = Client(transport=sample_transport, fetch_schema_from_transport=True,)
    return _client


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

    updated_at_md = "Repository updated on {date}.".format(
        date=datetime.now(timezone.utc).strftime("%A, %d. %B %Y")
    )

    rewritten = replace_chunk(readme_content, "updated_at", updated_at_md)

    readme.open("w").write(rewritten)
