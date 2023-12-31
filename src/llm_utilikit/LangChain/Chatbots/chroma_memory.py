import logging
from typing import List, Any, Dict
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings, HuggingFaceEmbeddings
from langchain.filters import EmbeddingsRedundantFilter
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
import chromadb
from langchain.vectorstores import Chroma

logging.basicConfig(level=logging.ERROR)

class ChromaMemory:
    def __init__(self, model_name: str, cache_dir: str, max_history_len: int, vectorstore: Chroma):
        """
        Initialize the ChromaMemory with a model name, cache directory, maximum history length, and a vectorstore.
        Args:
            model_name (str): The name of the LLM model to use.
            cache_dir (str): The path to the directory to cache embeddings.
            vectorstore (Chroma): The vectorstore to use for similarity matching.
            chroma_memory = ChromaMemory(model_name, cache_dir, max_history_len, vectorstore)
            max_history_len (int): The maximum length of the conversation history to remember.

        """
        try:
            self.embeddings = CacheBackedEmbeddings(
                OpenAIEmbeddings(model_name),
                cache_dir
            )
            self.filter = EmbeddingsRedundantFilter()
            self.chat_model = ChatOpenAI(
                self.embeddings,
                self.filter
            )
            self.memory = ConversationBufferWindowMemory(
                max_history_len,
                self.chat_model
            )
            self.retrieval = RetrievalQA(
                self.memory,
                vectorstore
            )
        except Exception as e:
            logging.error(f"Error initializing ChromaMemory: {e}")
            raise ValueError(f"Error initializing ChromaMemory: {e}") from e