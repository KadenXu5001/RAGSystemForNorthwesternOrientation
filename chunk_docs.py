"""
Step 2 — Read cleaned .txt files from documents/ and split into chunks.

Run this after you have manually cleaned the .txt files produced by fetch_docs.py.
Output: documents/chunks.json
"""

import json
import re
from pathlib import Path

CHUNK_SIZE = 400
OVERLAP = 100


def chunk(text: str, size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    """Split text into overlapping character-level chunks."""
    # Normalize whitespace so manual edits don't create uneven spacing
    text = re.sub(r"\s+", " ", text).strip()
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start += size - overlap
    return chunks


def main():
    docs_dir = Path("documents")
    txt_files = sorted(docs_dir.glob("*.txt"))

    if not txt_files:
        print("No .txt files found in documents/. Run fetch_docs.py first.")
        return

    all_chunks: list[dict] = []

    for path in txt_files:
        text = path.read_text(encoding="utf-8")
        file_chunks = chunk(text)
        print(f"{path.name:<40}  {len(file_chunks):>4} chunks  ({len(text)} chars)")

        for i, c in enumerate(file_chunks):
            all_chunks.append(
                {
                    "source_file": path.name,
                    "chunk_index": i,
                    "text": c,
                }
            )

    out_path = docs_dir / "chunks.json"
    out_path.write_text(json.dumps(all_chunks, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nDone. {len(all_chunks)} total chunks → {out_path}")
    print(f"Chunk size: {CHUNK_SIZE} chars | Overlap: {OVERLAP} chars")


if __name__ == "__main__":
    main()
