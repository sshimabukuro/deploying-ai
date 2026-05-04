import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import pandas as pd
from dotenv import load_dotenv
from utils.logger import get_logger
import os
from pathlib import Path
from openai import OpenAI

CSV_FILE = "./assignment_chat/channels_in_IT.csv"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "youtube_channels"

_logs = get_logger(__name__)
load_dotenv(".secrets")


def build_document(row: pd.Series) -> str:
    """
    Create the text that ChromaDB will embed and search semantically.

    We include the most meaningful searchable fields.
    """
    return (
        f"Channel Name: {row['Channel Name']}\n"
        f"Search Country: {row['Search Country']}\n"
        f"Country Code: {row['Country Code']}\n"
        f"Channel Country: {row['Country']}\n"
        f"Description: {row['Description']}"
    )


def import_csv_to_chroma() -> None:
    """
    Read the CSV file and import rows into a persistent ChromaDB collection.
    """

    csv_path = Path(CSV_FILE)

    if not csv_path.exists():
        _logs.error(f"CSV file not found: {CSV_FILE}")
        raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")

    df = pd.read_csv(csv_path)

    ids = []
    documents = []
    metadatas = []

    for index, row in df.iterrows():
        search_country = str(row["Search Country"])
        channel_id = str(row["Channel ID"])
        channel_name = str(row["Channel Name"])
        channel_country = str(row["Country"])
        country_rank = int(row["Country Rank"])
        description = str(row["Description"])

        ids.append(f"youtube_channel_{index}")

        documents.append(build_document(row))

        metadatas.append({
            "search_country": search_country,
            "channel_id": channel_id,
            "channel_name": channel_name,
            "channel_country": channel_country,
            "country_rank": country_rank,
            "description": description,
        })

    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    existing_collections = [collection.name for collection in chroma_client.list_collections()]

    if COLLECTION_NAME in existing_collections:
        _logs.info(f"Deleting existing collection: {COLLECTION_NAME}")
        chroma_client.delete_collection(name=COLLECTION_NAME)    

    collection = chroma_client.create_collection(
        name=COLLECTION_NAME,
        embedding_function = OpenAIEmbeddingFunction(
            api_key = "any value",
            model_name="text-embedding-3-small",
            api_base='https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1',
            default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')}
    ))

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    _logs.info(f"Imported {len(ids)} rows into ChromaDB collection: {COLLECTION_NAME}")
    _logs.info(f"ChromaDB persisted at: {CHROMA_PATH}")
    
    # chroma_client.delete_collection(name=COLLECTION_NAME)

    # _logs.info("Deleted collection: youtube_channels")
    # _logs.info("List of collections:", chroma_client.list_collections())

if __name__ == "__main__":
    import_csv_to_chroma()
