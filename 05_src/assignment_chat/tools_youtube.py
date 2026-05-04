from langchain.tools import tool
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from utils.logger import get_logger
import os

_logs = get_logger(__name__)
load_dotenv()
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


class YoutubeChannelData(BaseModel):
    """Structured channel data response."""
    channel_name: str = Field(..., description="The name of the Youtube channel.")
    channel_id: str = Field(..., description="The id of the Youtube channel.")
    description: str = Field(..., description="The Youtube channel description that is relevant to the user query.")
    country_rank: int = Field(None, description="The rank of the channel in its country.")


@tool
def recommend_youtube_channels(query: str, n_results: int = 1) -> list[YoutubeChannelData]:
    """
    Fetches top youtube channels based on the query. 
    Returns n_results channels.
    """
    recommendations = get_context(query, collection, n_results)
    return recommendations


def get_context(query:str, collection:chromadb.api.models.Collection, top_n:int):
    results = collection.query(
        query_texts=[query],
        n_results=top_n,
        include=["documents", "metadatas", "distances"]
    )
    recommendations = []    
    for i, metadata in enumerate(results["metadatas"][0]):
        _logs.debug(f"\nResult {i + 1}")
        _logs.debug(f"Channel: {metadata['channel_name']}")
        _logs.debug(f"Country Rank: {metadata['country_rank']}")
        _logs.debug(f"Distance: {results['distances'][0][i]}")
        _logs.debug(f"Description: {results['documents'][0][i][:200]}")
        try:
            rec = YoutubeChannelData(
                channel_name=metadata["channel_name"],
                channel_id=metadata["channel_id"],
                description=metadata["description"],
                country_rank=metadata["country_rank"]
            )
            recommendations.append(rec)
        except Exception as e:
            _logs.error(f"Error processing channel data: {e}")
            continue
    return recommendations