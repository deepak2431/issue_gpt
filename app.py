from helpers.github_helpers import GithubAPI
from helpers.open_ai_helpers import SearchIssue

from pprint import pprint
import json

repo_name = "deepak2431/djangoBlog"

github_api = GithubAPI(repo_name=repo_name)
df = github_api.get_issues()

issue_searcher = SearchIssue(df)
issue_searcher.generate_embeddings()
similar_issue = issue_searcher.find_similar_issues(new_issue="draft post", n=3)


with open("result.json", "w") as f:
    json.dump(similar_issue, f, indent=4)
