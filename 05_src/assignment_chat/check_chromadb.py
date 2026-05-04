import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv(".secrets")

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "youtube_channels"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_collection(
    name=COLLECTION_NAME,
    embedding_function = OpenAIEmbeddingFunction(
        api_key = "any value",
        model_name="text-embedding-3-small",
        api_base='https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1',
        default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')}
))


results = collection.query(
    query_texts=["Which channels are about music or news order by country rank?"],
    n_results=3,
    include=["documents", "metadatas", "distances"]
)

for i, metadata in enumerate(results["metadatas"][0]):
    print("\nResult", i + 1)
    print("Channel:", metadata["channel_name"])
    print("Country Rank:", metadata["country_rank"])
    print("Distance:", results["distances"][0][i])
    print(results["documents"][0][i][:200])