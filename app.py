from helpers.github_helpers import get_issues
from helpers.open_ai_helpers import generate_embeddings, find_similar_issues


df = get_issues("deepak2431/issue_checker")


embeddings = res = generate_embeddings(df, 'generated embeddings', n=3)
print(embeddings)


"""# Replace 'your_prompt' with the text you want to find similar issues for
prompt = "tell me the issues which are similiar to code for generating embeddings"
similar_issues = find_similar_issues(prompt, embeddings)

print("Similar issues:")
for index, similarity_score in similar_issues:
    issue = df[index]
    print(f"Issue title: {issue['issue_title']}, Similarity score: {similarity_score}")"""
