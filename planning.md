# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

I choose Wildcat welcome, because it is our school's oreintation and there are a lot of stuff that is midly touched on at the start of the year, and then forgotten about. There are a lot of good resources there, so that could be useful.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #   | Source                                  | Description                                              | URL or location                                                                                                                                        |
| --- | --------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| 1   | Wildcat welcome page                    | Describes the gist of wildcat welcome                    | https://www.northwestern.edu/newstudent/first-year-students/wildcat-welcome/                                                                           |
| 2   | Student newspaper about wildcat welcome | A student newspaper about wildcat welcome and what to do | https://dailynorthwestern.com/2025/08/31/featured-stories/orientationissue/orientation-issue-2025/welcoming-the-wildcats-a-rundown-on-wildcat-welcome/ |
| 3   | New student move in page                | page where housing/move in details are kept              |                                                                                                                                                        | https://www.northwestern.edu/living/incoming-undergraduates/new-student-and-transfer-student-fall-move-in.html |
| 4   | Wildcat welcome FAQs                    | FAQs for wildcat welcome                                 | https://www.northwestern.edu/newstudent/about/faqs/faqs-wildcat-welcome.html                                                                           |
| 5   | International student programming guide | Guide for programing for international students          | https://www.northwestern.edu/purple-prep/orientation/international-student-orientation.html                                                            |
| 6   | student resources                       | links to several student resources on campus             | https://www.northwestern.edu/newstudent/first-year-students/                                                                                           |
| 7   | Northwestern Academic calandar          | academic calandar                                        | https://www.registrar.northwestern.edu/calendars/academic-calendars/                                                                                   |
| 8   | Systems and apps                        | Info about what apps you need to download                | https://www.northwestern.edu/purple-prep/prepare/systems-apps.html                                                                                     |
| 9   | Peer advisor guide                      | Webpage about what to expect for peer advisors           | https://www.northwestern.edu/studentaffairs/news-events/pa-program.html                                                                                |
| 10  | Health requirements                     | Guide to which immunizaitons are required to attend      | https://www.northwestern.edu/immunization-compliance/required-immunizations/new-undergraduate-and-graduate-students.html                               |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

I think that 400 characters chuncks are good, since our pages are normally quite short bits of information, so anymore may reduce the quality of our chunks.

**Overlap:**
The overlap should be around 100 characters. I think although this is a lot, a couple of the pages have much longer paragraphs than others, so this should make it so that everything coherent be covered.

**Reasoning:**

See above.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

I probably keep all-MiniLM-L6-v2 via sentence-transformers

**Top-k:**

top 3 should be sufficient. Maybe even 2, if we're risky

**Production tradeoff reflection:**

If cost wasn't a constraint, I would consider the dimentionality of the vectors. Mainly, I would probably decide how "in-depth" my vector embeddings have to be. I think that in this case, since a lot of my sources deal with different topics, a small amount of dimentions should be enough, but if my scope was more narrow/percise or I had a couple of similar sources, I might prefer higher dimentioned embeddings.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| #   | Question                                                   | Expected answer                                                       |
| --- | ---------------------------------------------------------- | --------------------------------------------------------------------- |
| 1   | How many doses of DTP, DTaP, DT, Td, or Tdap are required. | Up to 3                                                               |
| 2   | When are purple prep emails sent out                       | The first and third Tuesday of every month from May through September |
| 3   | When do first year students register for classes?          | during Wildcat Welcome                                                |
| 4   | where you access services and requests related to housing  | The housing portal                                                    |
| 5   | When do fall classes begin?                                | Wednesday, September 23, 2026                                         |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Difficulty parsing the documents, since some might have pictures or hyperlinks in them that might distract the model or chew up characters with little value.

2. Some of the documents are FAQ pages and others are longer documents, and one is a slide show, so the optimal chunking for each page seems to be quite different, which may run into problems in the future

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     Document Ingestion          Chunking              Embedding + Vector Store         Retrieval              Generation

────────────────── ────────────── ──────────────────────── ───────────── ──────────────────

Web Scraping Text Split all-MiniLM-L6-v2 Cosine Claude API
(requests / (400 char chunks, ────────────────────────── Similarity (claude-sonnet)
BeautifulSoup) 100 char overlap) Convert chunks to vectors Search │
│ │ │ │ │
▼ ▼ ▼ ▼ ▼
┌─────────────┐ ┌──────────────────┐ ┌────────────────────┐ ┌───────────────┐ ┌──────────────────────┐
│ 10 Source │──────▶ │ Raw Text Split │────▶ │ ChromaDB / │────▶│ Top-k = 3 │────▶│ Answer + Source │
│ URLs │ │ into Chunks │ │ FAISS Vector │ │ Chunks │ │ Attribution │
└─────────────┘ └──────────────────┘ │ Store │ └───────────────┘ └──────────────────────┘
└────────────────────┘

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
