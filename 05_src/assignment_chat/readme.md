# Assignment 2:

The goal of this assignment is to design and implement an AI system with a conversational interface.
This implementation is based on LangGraph's tools. The tools node uses LangGraph's `ToolNode` class and 
`tools_condition` is the standard tool stopping criteria.
 
## Services

The file main.py contains the llm model calls that controls the chat. Tools are in the files tools_*.py.
Three services are implemented.

### Service 1: Weather API Call

+ The [weatherstack API](https://weatherstack.com/?utm_source=Github&utm_medium=Referral&utm_campaign=Public-apis-repo-Best-sellers) is one of the [public and free APIs on GitHub](https://github.com/public-apis/public-apis).
+ The weatherstack service retrieve instant, accurate weather information for any location in the world in lightweight JSON format.
+ The free plan allows 100 calls/month.
+ This is a simple tool implementation that returns a string with the weather condition and temperature. 

### Service 2: Semantic Query

+ The semantic query uses a [ChromaDB instance with file persistence](https://docs.trychroma.com/docs/run-chroma/persistent-client)
+ The data source for the ChromaDB is the [Kaggle](https://www.kaggle.com/) dataset [Top YouTube Channels: Global & Country-Wise (2026)](https://www.kaggle.com/datasets/yusufmurtaza01/youtube-top-channels-2026) for Italy. The dataset `channels_in_IT.csv` lists the top 100 trending YouTube channels in Italy. 
+ The `create_chromadb.py` was created to produce the embeddings. In simple terms: CSV → searchable text + metadata → embeddings → persistent ChromaDB collection for semantic search. 
+ The `check_chromadb.py` was created to run a quick test on the ChromaDB.

### Service 3: Web Search

+ The [zenserp API](https://zenserp.com/?utm_source=Github&utm_medium=Referral&utm_campaign=Public-apis-repo-Best-sellers) is one of the [public and free APIs on GitHub](https://github.com/public-apis/public-apis).
+ The zenserp service retrieve fast, accurate Google Search data built for developers.
+ The free plan allows 50 searches/month.
+ This is a tool implementation that returns a [Pydantic](https://docs.pydantic.dev/latest/) Model.

## User Interface

+ Added conversational style.
+ Implemented in Gradio

---

## Guardrails and Other Limitations

* Included guardrails that prevent users from:

  * Accessing or revealing the system prompt.
  * Modifying the system prompt directly.

* The model must not respond to questions on certain restricted topics:

  * Cats or dogs
  * Horoscopes or Zodiac Signs
  * Taylor Swift



