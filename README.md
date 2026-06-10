# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section _after_ you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

I choose Wildcat welcome, because it is our school's oreintation and there are a lot of stuff that is midly touched on at the start of the year, and then forgotten about. There are a lot of good resources there, so that could be useful.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

I think that 400 characters chuncks are good, since our pages are normally quite short bits of information, so anymore may reduce the quality of our chunks.

**Overlap:**
The overlap should be around 75 characters. I think although this is a lot, a couple of the pages have much longer paragraphs than others, so this should make it so that everything coherent be covered.

**Why these choices fit your documents:**

These choicse fit the documents since most of them are FAQ documents, so it doens't really need a massive context since the answers will likely be a sentence long. 400 characters aren't that long in the grand scheme of things.

**Final chunk count:**
293

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| #   | Question                                                   | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
| --- | ---------------------------------------------------------- | --------------- | ---------------------------- | ----------------- | ----------------- |
| 1   | How many doses of DTP, DTaP, DT, Td, or Tdap are required. | up to 3         | up to 3                      | Relevent          | accurate          |

|
2 | When are purple prep emails sent out | first and third Tuesday of every month from May through September | launches in early may | relevent | partially accurate |
| 3 |When do first year students register for classes? | during wildcat welcome|during wildcat welcome |relevent |accurate |
| 4 |where can I learn more about housing | The housing portal| various accurate resources about housing | relvent |accurate |
| 5 | When do fall classes begin? |Wednesday, September 23, 2026 | not enough informatoin| partially relevent| inaccurate|

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
When do fall classes begin?
**What the system returned:**
I don't have enough information on that.
**Root cause (tied to a specific pipeline stage):**

In the chunking, the target chunk that would have it (07 academic calander chunk 9) isn't found. Instead, the winter classes
and when they start are found instead. The retreival stage/chunking stage is to blame.

**What you would change to fix it:**

I would probably have to do a more through search & clense through the chunking. I realized that the academic calandar document lists the date and then the event afterwards, but it might be hard to pickout which date is to which event due to chunking since there isn't a really clear indicator (ie a colon :) to determine which date corresponds to which event

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- _What I gave the AI:_
- _What it produced:_
- _What I changed or overrode:_

**Instance 2**

- _What I gave the AI:_
- _What it produced:_
- _What I changed or overrode:_
