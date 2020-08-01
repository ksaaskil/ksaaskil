from . import build_readme


EXAMPLE_REPOS_RESPONSE = {
    "viewer": {
        "repositories": {
            "totalCount": 71,
            "nodes": [
                {
                    "name": "shc-python-tools",
                    "forkCount": 3,
                    "url": "https://github.com/ksaaskil/shc-python-tools",
                    "updatedAt": "2020-07-23T16:28:19Z",
                    "stargazers": {"totalCount": 7},
                },
                {
                    "name": "functional-programming-examples",
                    "forkCount": 0,
                    "url": "https://github.com/ksaaskil/functional-programming-examples",
                    "updatedAt": "2020-08-01T11:59:15Z",
                    "stargazers": {"totalCount": 4},
                },
                {
                    "name": "fp-gitlab-example",
                    "forkCount": 1,
                    "url": "https://github.com/ksaaskil/fp-gitlab-example",
                    "updatedAt": "2020-06-03T00:06:52Z",
                    "stargazers": {"totalCount": 3},
                },
                {
                    "name": "introduction-to-property-based-testing",
                    "forkCount": 0,
                    "url": "https://github.com/ksaaskil/introduction-to-property-based-testing",
                    "updatedAt": "2020-04-14T08:04:54Z",
                    "stargazers": {"totalCount": 2},
                },
                {
                    "name": "liquid-solid",
                    "forkCount": 1,
                    "url": "https://github.com/ksaaskil/liquid-solid",
                    "updatedAt": "2020-01-07T15:40:18Z",
                    "stargazers": {"totalCount": 1},
                },
            ],
        }
    }
}


def test_to_repository():
    count, repos = build_readme.gql_response_to_repositories(EXAMPLE_REPOS_RESPONSE)
    assert count == 71
    assert len(repos) == 5


def test_to_repo_content():
    count, repos = build_readme.gql_response_to_repositories(EXAMPLE_REPOS_RESPONSE)
    content = build_readme.build_repositories_content(count, repos)
    assert isinstance(content, str)
    for repo in repos:
        assert repo.name in content, f"Expected to find {repo.name} in new content"
