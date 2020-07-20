"""
Inspired by https://github.com/simonw/simonw/blob/main/build_readme.py
"""
import pathlib
import os

from python_graphql_client import GraphqlClient


root = pathlib.Path(__file__).parent.resolve()
client = GraphqlClient(endpoint="https://api.github.com/graphql")

TOKEN = os.environ.get("API_TOKEN", "")

if __name__ == "__main__":
    readme = root / "README.md"

    readme_content = readme.open("r").read()

    new_readme_content = readme_content  # TODO

    readme.open("w").write(new_readme_content)
