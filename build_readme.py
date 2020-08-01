"""
Inspired by and some of the code copied from
https://github.com/simonw/simonw/blob/main/build_readme.py.

GraphQL queries, parsing, and tests written by me.
"""
from datetime import datetime, timezone
from dataclasses import dataclass
import pathlib
import os
import re
import typing

from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

load_dotenv()

root = pathlib.Path(__file__).parent.resolve()


TOKEN = os.environ.get("API_TOKEN", "")

_client: Client = None

REPOSITORIES_QUERY = gql(
    """
query($number_of_repos:Int!) {
  viewer {
     repositories(first: $number_of_repos, orderBy: {field:STARGAZERS, direction:DESC}) {
       totalCount
       nodes {
         name
         forkCount
		 url
         stargazers {
          totalCount
         }
       }
     }
   }
}
"""
)


@dataclass(frozen=True)
class Repository:
    name: str
    stars: int
    forks: int
    url: str


def gql_response_to_repositories(
    data: dict,
) -> typing.Tuple[int, typing.Sequence[Repository]]:
    repositories = data["viewer"]["repositories"]
    count = repositories["totalCount"]
    nodes = repositories["nodes"]
    return (
        count,
        [
            Repository(
                name=repo["name"],
                stars=repo["stargazers"]["totalCount"],
                forks=repo["forkCount"],
                url=repo["url"],
            )
            for repo in nodes
        ],
    )


def get_repositories(count=5):
    client = get_client()
    params = {"number_of_repos": count}
    response_data = client.execute(REPOSITORIES_QUERY, variable_values=params)
    return gql_response_to_repositories(response_data)


def get_client():

    global _client

    if _client is not None:
        return _client

    if TOKEN == "":
        raise Exception("API_TOKEN not defined")

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


def build_repositories_content(count: int, repos: typing.Sequence[Repository]) -> str:
    def repo_to_line(repo):
        return f"|[{repo.name}]({repo.url})|{repo.stars}|{repo.forks}"

    return f"""
## Repositories ({count} in total)
| Name        | Stars           | Forks  |
| ------------- |-------------| -----|
{os.linesep.join([repo_to_line(repo) for repo in repos])}
"""


if __name__ == "__main__":
    readme = root / "README.md"

    total_count, repositories = get_repositories()

    repositories_content = build_repositories_content(total_count, repositories)

    readme_content = readme.open("r").read()

    updated_at_md = "Table updated on {date}.".format(
        date=datetime.now(timezone.utc).strftime("%A, %d. %B %Y")
    )

    rewritten = replace_chunk(readme_content, "updated_at", updated_at_md)

    rewritten = replace_chunk(rewritten, "repositories", repositories_content)

    readme.open("w").write(rewritten)
