"""
Step 1 — Fetch and save each source as a .txt file in documents/.

Run this, then manually clean each file, then run chunk_docs.py.
"""

import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URLS = [
    {"id": 1,  "slug": "wildcat-welcome",           "url": "https://www.northwestern.edu/newstudent/first-year-students/wildcat-welcome/"},
    {"id": 2,  "slug": "daily-northwestern",         "url": "https://dailynorthwestern.com/2025/08/31/featured-stories/orientationissue/orientation-issue-2025/welcoming-the-wildcats-a-rundown-on-wildcat-welcome/"},
    {"id": 3,  "slug": "move-in",                    "url": "https://www.northwestern.edu/living/incoming-undergraduates/new-student-and-transfer-student-fall-move-in.html"},
    {"id": 4,  "slug": "wildcat-welcome-faqs",       "url": "https://www.northwestern.edu/newstudent/about/faqs/faqs-wildcat-welcome.html"},
    {"id": 5,  "slug": "international-orientation",  "url": "https://www.northwestern.edu/purple-prep/orientation/international-student-orientation.html"},
    {"id": 6,  "slug": "student-resources",          "url": "https://www.northwestern.edu/newstudent/first-year-students/"},
    {"id": 7,  "slug": "academic-calendar",          "url": "https://www.registrar.northwestern.edu/calendars/academic-calendars/"},
    {"id": 8,  "slug": "systems-apps",               "url": "https://www.northwestern.edu/purple-prep/prepare/systems-apps.html"},
    {"id": 9,  "slug": "peer-advisor",               "url": "https://www.northwestern.edu/studentaffairs/news-events/pa-program.html"},
    {"id": 10, "slug": "health-requirements",        "url": "https://www.northwestern.edu/immunization-compliance/required-immunizations/new-undergraduate-and-graduate-students.html"},
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; NorthwesternGuideBot/1.0)"}


def fetch(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.text


def clean(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer",
                     "aside", "noscript", "form", "button", "iframe"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    # Collapse blank lines to at most one blank line
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip lines that are pure whitespace
    lines = [line.strip() for line in text.splitlines()]
    lines = [l for l in lines if l]
    return "\n".join(lines)


def main():
    out_dir = Path("documents")
    out_dir.mkdir(exist_ok=True)

    for source in URLS:
        filename = f"{source['id']:02d}_{source['slug']}.txt"
        out_path = out_dir / filename
        print(f"[{source['id']:2d}] Fetching {source['slug']} ...", end=" ", flush=True)
        try:
            html = fetch(source["url"])
            text = clean(html)
            out_path.write_text(text, encoding="utf-8")
            print(f"saved -> {filename}  ({len(text)} chars)")
        except Exception as exc:
            print(f"ERROR — {exc}")
        time.sleep(0.5)

    print(f"\nDone. Edit the .txt files in documents/ then run chunk_docs.py.")


if __name__ == "__main__":
    main()
