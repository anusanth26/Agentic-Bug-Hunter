from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pathlib import Path

class MCPClient:
    """
    Read-only MCP client that queries the same vector index
    used by the MCP server.
    """

    def __init__(self):
        # 1️⃣ Set the SAME embedding model as the server
        embed_model_path = Path("../server/embedding_model")

        embed_model = HuggingFaceEmbedding(
            model_name=str(embed_model_path)
        )
        Settings.embed_model = embed_model

        # 2️⃣ Load existing storage (NO rebuilding)
        storage_context = StorageContext.from_defaults(
            persist_dir="../server/storage"
        )

        index = load_index_from_storage(storage_context)

        # 3️⃣ Create retriever
        self.retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=3
        )

    def search_bug_manual(self, query: str):
        nodes = self.retriever.retrieve(query)
        return [
            {"text": n.get_text(), "score": n.get_score()}
            for n in nodes
        ]
