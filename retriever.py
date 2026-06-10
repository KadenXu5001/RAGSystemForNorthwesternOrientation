"""
Milestone 4 — Embedding and retrieval.

Loads chunks from documents/chunks.json, embeds them with all-MiniLM-L6-v2
via sentence-transformers, stores them in a persistent ChromaDB collection,
and provides a retrieve() function for semantic search.
"""

import json
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

# ── Configuration ─────────────────────────────────────────────────────────────

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "unofficial_guide"
CHUNKS_PATH = Path("documents/chunks.json")
N_RESULTS = 5

# ── Initialization ─────────────────────────────────────────────────────────────
# sentence-transformers downloads the model on first use (~20 MB).
# Subsequent runs use a local cache.

_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


# ── Public API ─────────────────────────────────────────────────────────────────


def load_chunks() -> list[dict]:
    """Load all chunks from the JSON file produced by chunk_docs.py / ingest.py."""
    return json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))


def embed_and_store(chunks: list[dict] | None = None) -> None:
    """
    Embed chunks and store them in ChromaDB with source metadata.

    Loads from documents/chunks.json when chunks is not provided.
    Each chunk is stored with:
      - document : raw text (ChromaDB's embedding function converts this to a vector)
      - metadata : source_file (document name) and chunk_index (position in source)
      - id       : "<source_file>_<chunk_index>" for stable deduplication

    Skips ingestion if the collection is already populated — delete ./chroma_db
    and re-run to force a fresh ingest.
    """
    if _collection.count() > 0:
        print(f"Collection already has {_collection.count()} chunks. Skipping ingestion.")
        print("Delete ./chroma_db and restart to re-ingest.")
        return

    if chunks is None:
        chunks = load_chunks()

    # Build the source_file field: chunk_docs.py uses "source_file",
    # ingest.py uses "source_label" — support both.
    def _source(c: dict) -> str:
        return c.get("source_file") or c.get("source_label", "unknown")

    ids = [f"{_source(c)}_{c['chunk_index']}" for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [
        {
            "source_file": _source(c),
            "chunk_index": c["chunk_index"],
        }
        for c in chunks
    ]

    _collection.add(documents=documents, metadatas=metadatas, ids=ids)
    print(f"Stored {_collection.count()} chunks in ChromaDB ({EMBEDDING_MODEL}).")


def retrieve(query: str, n_results: int = N_RESULTS) -> list[dict]:
    """
    Return the top-k chunks most semantically similar to query.

    Each result dict contains:
      - text        : chunk text
      - source_file : originating document filename
      - chunk_index : position of this chunk within its source document
      - distance    : cosine distance (lower = more similar)
    """
    if _collection.count() == 0:
        return []

    results = _collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    # _collection.query() returns nested lists (one per query in query_texts).
    # Index [0] extracts results for our single query.
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    chunks = []
    for text, meta, dist in zip(documents, metadatas, distances):
        chunks.append(
            {
                "text": text,
                "source_file": meta["source_file"],
                "chunk_index": meta["chunk_index"],
                "distance": dist,
            }
        )
        print(
            f"[{meta['source_file']} chunk {meta['chunk_index']}] "
            f"(dist: {dist:.3f}) {text[:80]}…"
        )

    return chunks


# ── Quick smoke test ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    embed_and_store()
    print()

    test_queries = [
        "When do fall classes begin?",
        "When do first year students register for classes?",
        "What immunizations are required?",
    ]

    for q in test_queries:
        print(f"Query: {q}")
        for r in retrieve(q):
            print(
                f"  [{r['source_file']} #{r['chunk_index']}] "
                f"dist={r['distance']:.3f}  {r['text'][:100]}…"
            )
        print()
