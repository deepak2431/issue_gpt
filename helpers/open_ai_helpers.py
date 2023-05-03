import os
import json
from dotenv import load_dotenv

import openai
from pprint import pprint

from openai.embeddings_utils import get_embedding, cosine_similarity

from github import Github

load_dotenv()

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191


def generate_embeddings(df, pprint=True):
    df["combined"] = (
        "Issue description: "
        + df.issue_description.str.strip()
        + "; Issue Title: "
        + df.issue_title.str.strip()
    )

    embedding = get_embedding(df, model='text-embedding-ada-002')
    df['similarities'] = df.ada_embedding.apply(lambda x: cosine_similarity(x, embedding))
    res = df.sort_values('similarities', ascending=False).head(n)
    return res


def find_similar_issues(prompt, embeddings, threshold=0.8):
    similar_issues = []

    # Generate an embedding for the prompt text
    response = openai.Completion.create(
        engine="text-embedding-ada-002",
        prompt=f"Generate a 50-dimensional embedding for the following text: {prompt}",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    prompt_embedding = response.choices[0].text.strip()

    # Compare the prompt embedding with existing embeddings
    for index, embedding in enumerate(embeddings):
        similarity = openai.Completion.create(
            engine="text-embedding-ada-002",
            prompt=f"Compute the cosine similarity between the following two embeddings:\nEmbedding 1: {prompt_embedding}\nEmbedding 2: {embedding}\nSimilarity:",
            max_tokens=10,
            n=1,
            stop=None,
            temperature=0.5,
        )

        similarity_score = float(similarity.choices[0].text.strip())
        if similarity_score >= threshold:
            similar_issues.append((index, similarity_score))

    # Sort the similar issues by their similarity score
    similar_issues.sort(key=lambda x: x[1], reverse=True)
    return similar_issues
