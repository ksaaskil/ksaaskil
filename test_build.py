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
                    "pushedAt": "2019-03-15T10:04:50Z",
                    "stargazers": {"totalCount": 7},
                },
                {
                    "name": "functional-programming-examples",
                    "forkCount": 0,
                    "url": "https://github.com/ksaaskil/functional-programming-examples",
                    "pushedAt": "2020-08-01T11:59:16Z",
                    "stargazers": {"totalCount": 4},
                },
                {
                    "name": "fp-gitlab-example",
                    "forkCount": 1,
                    "url": "https://github.com/ksaaskil/fp-gitlab-example",
                    "pushedAt": "2020-07-18T01:58:18Z",
                    "stargazers": {"totalCount": 3},
                },
                {
                    "name": "introduction-to-property-based-testing",
                    "forkCount": 0,
                    "url": "https://github.com/ksaaskil/introduction-to-property-based-testing",
                    "pushedAt": "2020-07-19T23:37:16Z",
                    "stargazers": {"totalCount": 2},
                },
                {
                    "name": "liquid-solid",
                    "forkCount": 1,
                    "url": "https://github.com/ksaaskil/liquid-solid",
                    "pushedAt": "2016-01-08T16:03:49Z",
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
