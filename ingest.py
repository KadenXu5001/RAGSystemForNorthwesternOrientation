"""
Milestone 3 — Ingestion and chunking.

Fetches each URL, strips HTML noise, and splits the cleaned text into
overlapping character-level chunks.  Results are saved to documents/chunks.json.

Chunk size : 400 characters  (per planning.md)
Overlap    : 100 characters  (per planning.md)
"""

import json
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ── Constants ────────────────────────────────────────────────────────────────

CHUNK_SIZE = 400
OVERLAP = 100

URLS = [
    {
        "id": 1,
        "label": "Wildcat Welcome page",
        "url": "https://www.northwestern.edu/newstudent/first-year-students/wildcat-welcome/",
    },
    {
        "id": 2,
        "label": "Daily Northwestern orientation issue 2025",
        "url": (
            "https://dailynorthwestern.com/2025/08/31/featured-stories/"
            "orientationissue/orientation-issue-2025/"
            "welcoming-the-wildcats-a-rundown-on-wildcat-welcome/"
        ),
    },
    {
        "id": 3,
        "label": "New student move-in page",
        "url": (
            "https://www.northwestern.edu/living/incoming-undergraduates/"
            "new-student-and-transfer-student-fall-move-in.html"
        ),
    },
    {
        "id": 4,
        "label": "Wildcat Welcome FAQs",
        "url": "https://www.northwestern.edu/newstudent/about/faqs/faqs-wildcat-welcome.html",
    },
    {
        "id": 5,
        "label": "International student orientation guide",
        "url": "https://www.northwestern.edu/purple-prep/orientation/international-student-orientation.html",
    },
    {
        "id": 6,
        "label": "Student resources — first-year students",
        "url": "https://www.northwestern.edu/newstudent/first-year-students/",
    },
    {
        "id": 7,
        "label": "Northwestern academic calendar",
        "url": "https://www.registrar.northwestern.edu/calendars/academic-calendars/",
    },
    {
        "id": 8,
        "label": "Systems and apps guide",
        "url": "https://www.northwestern.edu/purple-prep/prepare/systems-apps.html",
    },
    {
        "id": 9,
        "label": "Peer advisor program",
        "url": "https://www.northwestern.edu/studentaffairs/news-events/pa-program.html",
    },
    {
        "id": 10,
        "label": "Health and immunization requirements",
        "url": (
            "https://www.northwestern.edu/immunization-compliance/required-immunizations/"
            "new-undergraduate-and-graduate-students.html"
        ),
    },
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; NorthwesternGuideBot/1.0; "
        "+https://github.com/codepath-students)"
    )
}


# ── Helpers ──────────────────────────────────────────────────────────────────


def fetch(url: str, timeout: int = 15) -> str:
    """Return raw HTML for *url*, or raise on HTTP error."""
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def clean(html: str) -> str:
    """Extract plain text from HTML, dropping boilerplate tags."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove elements that add noise but no content
    for tag in soup(["script", "style", "nav", "header", "footer",
                     "aside", "noscript", "form", "button", "iframe"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    # Collapse runs of whitespace / newlines into a single space
    text = re.sub(r"\s+", " ", text).strip()
    return text


def chunk(text: str, size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    """Split *text* into overlapping character-level chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start += size - overlap
    return chunks


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    out_dir = Path("documents")
    out_dir.mkdir(exist_ok=True)

    all_chunks: list[dict] = []
    total = 0

    for source in URLS:
        print(f"[{source['id']:2d}] Fetching: {source['label']} …", end=" ", flush=True)
        try:
            html = fetch(source["url"])
            text = clean(html)
            source_chunks = chunk(text)
            total += len(source_chunks)
            print(f"{len(source_chunks)} chunks  ({len(text)} chars)")

            for i, c in enumerate(source_chunks):
                all_chunks.append(
                    {
                        "source_id": source["id"],
                        "source_label": source["label"],
                        "source_url": source["url"],
                        "chunk_index": i,
                        "text": c,
                    }
                )
        except Exception as exc:
            print(f"ERROR — {exc}")

        time.sleep(0.5)  # be polite to the servers

    out_path = out_dir / "chunks.json"
    out_path.write_text(json.dumps(all_chunks, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nDone.  {total} total chunks written to {out_path}")
    print(f"Chunk size: {CHUNK_SIZE} chars | Overlap: {OVERLAP} chars")


if __name__ == "__main__":
    main()
