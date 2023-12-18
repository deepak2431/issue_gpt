import os
import pinecone

from dotenv import load_dotenv

load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_KEY")
PINECONE_ENVIRONMENT = "issue_gpt-dev"


pinecone_client = pinecone.init(
    api_key=PINECONE_API_KEY, enviroment=PINECONE_ENVIRONMENT
)


class PineCone:
    """PineCone class for interacting with Pinecone vector database.

    Provides methods for creating, retrieving, and updating Pinecone vector
    indexes and vectors.
    """

    index_name = ""

    def __init__(self, index_name) -> None:
        self.create_index(index_name=index_name)
        self.index_name = index_name

    def create_index(self, index_name):
        pinecone_index = pinecone_client.create_index(index_name, dimension=1536)

        print(pinecone_index)

    def get_index(self):
        index = pinecone.Index(self.index_name)
        return index

    def save_vector_to_index(self, embeddings_id, embeddings_data):
        index = self.get_index()
        index.upsert([embeddings_id, embeddings_data])

    def retrieve_vector_from_index(self, embeddings_id):
        index = self.get_index()
        return index.fetch([embeddings_id])

    def update_embeddings():
        pass
