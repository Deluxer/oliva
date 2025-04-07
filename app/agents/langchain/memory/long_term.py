from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime
import uuid
import logging

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from qdrant_client import QdrantClient, models
from app.agents.config.qdrant import QdrantConfig

logger = logging.getLogger(__name__)

class LongTermMemoryStore():
    """Long-term memory store implementation using Qdrant for semantic search via LangChain"""

    def __init__(
        self,
        collection_name: Optional[str] = None,
        embedding_model: str = "text-embedding-3-small",
        embedding_dims: int = 1536,
    ):
        """Initialize the memory store with Qdrant connection and in-memory store"""
        config = QdrantConfig()
        
        try:
            self.embeddings = OpenAIEmbeddings(model=embedding_model, dimensions=embedding_dims)
        except Exception as e:
            logger.error(f"Failed to initialize embeddings: {e}")
            raise
            
        self.collection_name = collection_name or config.QDRANT_COLLECTION_NAME
        self.embedding_dims = embedding_dims
        
        url = config.QDRANT_URL.get_secret_value()
        api_key = config.QDRANT_API_KEY.get_secret_value()
        
        try:
            self.client = QdrantClient(
                url=url,
                api_key=api_key,
                timeout=10.0
            )
            
            # Check if collection exists, if not create it
            collections = self.client.get_collections().collections
            collection_names = [collection.name for collection in collections]
            
            if self.collection_name not in collection_names:
                logger.info(f"Creating new collection: {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.embedding_dims,
                        distance=models.Distance.COSINE
                    )
                )
                logger.info(f"Created new collection: {self.collection_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant store: {e}")
            raise

    def put(
        self,
        namespace: Union[Tuple[str, str], str],
        key: str,
        value: Dict[str, Any],
        *,
        index: Optional[Union[List[str], bool]] = None
    ) -> None:
        """Store a value in both Qdrant and in-memory store with semantic indexing
        
        Args:
            namespace: Either a tuple of (user_id, memory_type) or a string in format "user_id:memory_type"
            key: Unique identifier for the memory
            value: Dictionary containing the memory data
            index: List of fields to embed, or False to skip embedding
        """
        # Convert tuple namespace to string if needed
        if isinstance(namespace, tuple):
            namespace = f"{namespace[0]}:{namespace[1]}"

        if index is False:
            return
            
        try:
            fields_to_embed = index if isinstance(index, list) else ["memory"]
            
            texts_to_embed = []
            for field in fields_to_embed:
                if field in value:
                    field_value = value[field]
                    if isinstance(field_value, str):
                        texts_to_embed.append(field_value)
                    else:
                        texts_to_embed.append(str(field_value))
            
            text_to_embed = " ".join(texts_to_embed)
            if not text_to_embed.strip():
                logger.warning(f"No text to embed found in fields: {fields_to_embed}")
                return
                
            vector = self.embeddings.embed_query(text_to_embed)
            
            point_id = str(uuid.uuid4())
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=point_id,
                        payload={
                            "namespace": namespace,
                            "key": key,
                            "value": value,
                            "created_at": datetime.now().isoformat(),
                            "updated_at": datetime.now().isoformat(),
                            "embedded_fields": fields_to_embed
                        },
                        vector=vector
                    )
                ]
            )
            logger.info(f"Successfully stored vector with id {point_id} in Qdrant")
        except Exception as e:
            logger.error(f"Failed to store in Qdrant: {e}")

    def search(
        self,
        namespace: Union[Tuple[str, str], str],
        query: str,
        limit: int = 5,
        *,
        score_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Search for memories semantically similar to the query
        
        Args:
            namespace: Either a tuple of (user_id, memory_type) or a string in format "user_id:memory_type"
            query: Query text to search for
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score (0-1) for results
        
        Returns:
            List of memories with their similarity scores
        """
        # Convert tuple namespace to string if needed
        if isinstance(namespace, tuple):
            namespace = f"{namespace[0]}:{namespace[1]}"

        try:
            query_vector = self.embeddings.embed_query(query)
            
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=models.Filter(
                    should=[
                        models.FieldCondition(
                            key="namespace",
                            match=models.MatchValue(value=namespace)
                        )
                    ]
                ),
                limit=limit,
                score_threshold=score_threshold
            )

            results = []
            for hit in search_result:
                memory = hit.payload["value"]
                results.append({
                    "value": memory,
                    "score": hit.score,
                    "id": hit.id,
                    "created_at": hit.payload.get("created_at"),
                    "embedded_fields": hit.payload.get("embedded_fields", [])
                })
            
            logger.debug(f"Found {len(results)} similar memories")
            return results
            
        except Exception as e:
            logger.error(f"Failed to search memories: {e}", exc_info=True)
            return []
    
    def evaluate(self, query: str, memories: List[Dict[str, Any]]) -> Union[bool, str]:
        """Evaluate if the memories are relevant to the current query using LLM.
        
        Args:
            query: Current user query
            memories: List of retrieved memories with their metadata
            
        Returns:
            Union[bool, str]: Either a boolean indicating if memories are relevant,
                            or a string containing the refined response
        """
        try:
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            
            memory = memories[0]["value"]
            memory_query = memory["query"]
            memory_response = memory["response"]
            similarity_score = memories[0]["score"]

            eval_prompt = f"""Evaluate if a previous response can be reused for a new query and refine it if needed.

            Current Query: "{query}"

            Previous Interaction:
            Query: "{memory_query}"
            Response: "{memory_response}"
            Similarity Score: {similarity_score:.2f} (0-1 scale)

            Instructions:
            1. First, evaluate if the queries are asking for similar information (e.g., both about books, products, etc.)
            2. If queries are NOT similar, respond with "false"
            3. If queries ARE similar:
               - If ALL items in the previous response satisfy the current query's conditions, respond with "true"
               - If SOME items match but others don't, respond with a REFINED version of the response that includes ONLY the matching items
               - If NO items match the current query's conditions, respond with "false"
            
            Format your response as either:
            - "false" if responses are completely different or no items match
            - "true" if all items in the original response match
            - A refined response starting with "REFINED:" that includes only matching items in the same format as the original response

            Example refinements:
            REFINED:
            Here are some books priced under $20:
            1. **Book Title**
               - Price: $15.99
               - Rating: 4.5
            [Rest of the refined response...]

            REFINED:
            Harrison Chase defines an AI agent as...
            [Rest of the refined response...]
            """

            result = llm.invoke(eval_prompt)
            
            content = result.content.strip()
            if content.startswith("REFINED:"):
                # Return the refined response
                return content[8:].strip()  # Remove "REFINED:" prefix
            else:
                # Return boolean for true/false responses
                return content.lower() == "true"
            
        except Exception as e:
            logger.error(f"Failed to evaluate memories: {e}", exc_info=True)
            return False

long_term_memory = LongTermMemoryStore()