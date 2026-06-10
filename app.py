"""
RAG app — Wildcat Welcome orientation assistant.

Generation layer (Groq llama-3.3-70b-versatile) + Gradio UI wired to the
ChromaDB retriever built in retriever.py.

Run:
    python app.py
"""

import os

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

from retriever import retrieve

load_dotenv()

# ── LLM client ────────────────────────────────────────────────────────────────

_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

# ── Grounded system prompt ─────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a helpful assistant for Northwestern University's Wildcat Welcome "
    "orientation program. "
    "Answer ONLY using the documents provided in the user message below. "
    "Do not use any outside knowledge or information not present in those documents. "
    "If the documents do not contain enough information to answer the question, "
    "respond with exactly: 'I don't have enough information on that.' "
    "Do not guess, infer, or extrapolate beyond what the documents say."
)


# ── Core RAG function ──────────────────────────────────────────────────────────


def query_rag(question: str) -> tuple[str, list[str]]:
    """
    Retrieve relevant chunks, call the LLM, and return the answer with sources.

    Returns:
        answer  — LLM text response (grounded to retrieved context)
        sources — deduplicated list of source labels from the top-3 chunks
                  (programmatically extracted, not inferred by the LLM)
    """
    if not question.strip():
        return "Please enter a question.", []

    chunks = retrieve(question)

    if not chunks:
        return (
            "I don't have enough information on that. "
            "(The knowledge base appears to be empty — run retriever.py first.)",
            [],
        )

    # Build a numbered context block — the LLM sees only this, nothing else.
    context_lines = []
    for i, chunk in enumerate(chunks, start=1):
        context_lines.append(f"[Document {i}]\n{chunk['text']}")
    context_block = "\n\n".join(context_lines)

    user_message = (
        f"Documents:\n\n{context_block}\n\n"
        f"Question: {question}"
    )

    response = _groq.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0,  # deterministic; grounding requires no creative drift
    )

    answer = response.choices[0].message.content.strip()

    # Source attribution is programmatic — pulled from ChromaDB metadata,
    # never from whatever the LLM chose to mention.
    sources = list(dict.fromkeys(chunk["source_file"] for chunk in chunks))

    return answer, sources


# ── Gradio interface ───────────────────────────────────────────────────────────


def _run_query(question: str) -> tuple[str, str]:
    """Adapter between query_rag and Gradio outputs."""
    answer, sources = query_rag(question)
    if sources:
        sources_text = "\n".join(f"• {s}" for s in sources)
    else:
        sources_text = "(no sources retrieved)"
    return answer, sources_text


with gr.Blocks(title="Wildcat Welcome RAG Assistant") as demo:
    gr.Markdown("## Wildcat Welcome Orientation Assistant")
    gr.Markdown(
        "Ask any question about Northwestern's Wildcat Welcome orientation. "
        "Answers are grounded in official orientation documents only."
    )

    with gr.Row():
        question_box = gr.Textbox(
            label="Your question",
            placeholder="e.g. When do fall classes begin?",
            lines=2,
            scale=4,
        )

    submit_btn = gr.Button("Ask", variant="primary")

    answer_box = gr.Textbox(
        label="Answer",
        lines=6,
        interactive=False,
    )
    sources_box = gr.Textbox(
        label="Sources",
        lines=4,
        interactive=False,
    )

    submit_btn.click(
        fn=_run_query,
        inputs=question_box,
        outputs=[answer_box, sources_box],
    )
    question_box.submit(
        fn=_run_query,
        inputs=question_box,
        outputs=[answer_box, sources_box],
    )

if __name__ == "__main__":
    demo.launch()
