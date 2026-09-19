"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


# A sentence shorter than this absorbs the next one in its paragraph until it
# clears the line. 40 catches the 20% of campus_life sentences that say nothing
# on their own ("Not curved.", "Second-year here.") and leaves the median
# 63-character sentence exactly as it was written.
MIN_CHUNK_CHARS = 40

_PARAGRAPH_BREAK = re.compile(r"\n\s*\n")
_TERMINAL = re.compile(r"[.!?]+")


def _split_header(text: str) -> tuple[str, str]:
    """
    Peel the header line off the front of a document.

    A header is the first line when a blank line follows it — which is how all
    88 campus_life documents are laid out. Anything else is body all the way up.
    """
    lines = text.split("\n")
    if len(lines) > 1 and not lines[1].strip():
        return lines[0].strip(), "\n".join(lines[2:]).strip()
    return "", text.strip()


def _split_sentences(paragraph: str) -> tuple[list[str], str]:
    """
    Cut one paragraph at its terminal punctuation.

    Returns the sentences, plus whatever trailed after the last '.', '!' or '?'
    with no terminal mark of its own — the caller decides where that goes,
    because it may belong to a chunk from the paragraph before.

    A '.' is not a terminal mark when it sits between two digits ($1.75, 13.00)
    or when the next thing along is lowercase. That second rule is what an
    abbreviation looks like from here: "9 a.m. Monday" cuts after "a.m." and
    not after "a.", without needing a list of abbreviations to check against.
    """
    sentences: list[str] = []
    start = 0

    for match in _TERMINAL.finditer(paragraph):
        before = paragraph[match.start() - 1] if match.start() else ""
        rest = paragraph[match.end() :]

        if match.group() == "." and before.isdigit() and rest[:1].isdigit():
            continue
        if rest.lstrip()[:1].islower():
            continue

        sentence = paragraph[start : match.end()].strip()
        if sentence:
            sentences.append(sentence)
        start = match.end()

    return sentences, paragraph[start:].strip()


def _merge_short(sentences: list[str], minimum: int) -> list[str]:
    """
    Fold sentences too short to stand on their own into their neighbours.

    A short sentence takes the next one, and keeps taking until it is over the
    line. One with nothing after it goes backwards into the sentence before
    instead. A short sentence that is the whole paragraph stays as it is —
    there is nothing in the paragraph to join it to.
    """
    merged: list[str] = []
    pending = ""

    for sentence in sentences:
        pending = f"{pending} {sentence}" if pending else sentence
        if len(pending) >= minimum:
            merged.append(pending)
            pending = ""

    if pending:
        if merged:
            merged[-1] = f"{merged[-1]} {pending}"
        else:
            merged.append(pending)

    return merged


def _with_header(header: str, text: str) -> str:
    """Put the document's header on the front of a chunk: "header: text"."""
    if not header:
        return text
    separator = " " if header.endswith(":") else ": "
    return f"{header}{separator}{text}"


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    One sentence per chunk, each carrying its document's header.

    This is acceptance criterion 4. The documents here are short — 200 to 600
    characters — so a fixed-size window cuts sentences in half and loses the
    context the answer needed. Cutting at terminal punctuation instead means no
    chunk ever ends mid-thought.

    The rules, in order:
      - The first line of a document is its header when a blank line follows.
      - Paragraphs are split at blank lines and nothing is merged across one.
      - Inside a paragraph, text is cut at '.', '!' and '?' — but not at a
        period inside a number, a time or a decimal, and not at one an
        abbreviation put there. See `_split_sentences`.
      - A sentence under MIN_CHUNK_CHARS absorbs its neighbours until it
        isn't. See `_merge_short`.
      - Every chunk is prefixed "header: text", so a chunk retrieved on its
        own still says which document it came from.
    """
    chunks: list[Chunk] = []

    for doc in documents:
        header, body = _split_header(doc.text)
        texts: list[str] = []

        for paragraph in _PARAGRAPH_BREAK.split(body):
            paragraph = re.sub(r"\s+", " ", paragraph).strip()
            if not paragraph:
                continue

            sentences, leftover = _split_sentences(paragraph)

            if leftover and sentences:
                sentences[-1] = f"{sentences[-1]} {leftover}"
            elif leftover and texts:
                # Nothing in this paragraph to hang it on, so it goes onto the
                # last chunk of the paragraph before.
                texts[-1] = f"{texts[-1]} {leftover}"
                continue
            elif leftover:
                sentences = [leftover]

            texts.extend(_merge_short(sentences, MIN_CHUNK_CHARS))

        # A document with a header and no body at all: index the header rather
        # than dropping the file out of the corpus silently.
        if not texts and header:
            texts = [header]
            header = ""

        for index, text in enumerate(texts):
            chunks.append(
                Chunk(
                    text=_with_header(header, text),
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
